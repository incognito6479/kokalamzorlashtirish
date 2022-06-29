from django.contrib.postgres.indexes import BrinIndex, GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.db import models
from django.db.models import Case, F, Q, Sum, Value, When
from django.db.models.functions import Coalesce
from django.utils.translation import ugettext_lazy as _

from common.models import BaseModel
from pitomnik.models import Plant


class RegionManager(models.Manager):
    pass


class Region(BaseModel):
    name = models.CharField(max_length=512, blank=False, null=False)
    coordinates = models.JSONField(blank=True, null=True)
    code = models.IntegerField()
    objects = RegionManager()

    class Meta:
        verbose_name = _("Region")
        verbose_name_plural = _("Regions")

    def __str__(self):
        return f"{self.name}"


class DistrictQuerySet(models.QuerySet):
    def get_user_organization_districts(self, user):
        region = user.organization.region
        if region:
            return self.filter(region=user.organization.region)
        return self.all()

    def filter_by_region(self, region_id):
        return self.filter(region_id=region_id)


class District(BaseModel):
    name = models.CharField(max_length=512, blank=False, null=False)
    region = models.ForeignKey(
        Region,
        on_delete=models.CASCADE,
        related_name="districts",
    )
    objects = DistrictQuerySet.as_manager()

    class Meta:
        verbose_name = _("District")
        verbose_name_plural = _("Districts")

    def __str__(self):
        return f"{self.name}"


class RoadQuerySet(models.QuerySet):
    def sum_month_lte_by_param(self, year, month, param):
        return Sum(
            Coalesce(
                Case(
                    When(
                        Q(
                            yearly__monthly_prod__month__month__lte=month,
                            yearly__year__year=year,
                        ),
                        then=param,
                    ),
                    default=0,
                ),
                0,
            )
        )

    def sum_month_by_param(self, year, month, param):
        return Sum(
            Coalesce(
                Case(
                    When(
                        yearly__monthly_prod__month__month=month,
                        yearly__year__year=year,
                        then=param,
                    ),
                    default=0,
                ),
                0,
            )
        )

    def annotate_statistics(self, year, month):
        return self.annotate(
            yearly_plan_money=Sum(
                Coalesce(
                    Case(
                        When(
                            Q(yearly__year__year=year),
                            then="yearly__money_amount_plan",
                        )
                    ),
                    0,
                ),
                distinct=True,
            ),
            production_money_until_month=self.sum_month_lte_by_param(
                year, month, "yearly__monthly_prod__base_prod__money_amount"
            ),
            monthly_plan_sum_until_month=self.sum_month_lte_by_param(
                year, month, "yearly__monthly_prod__monthly_plan_money"
            ),
            monthly_financing_sum_until_month=self.sum_month_lte_by_param(
                year, month, "yearly__monthly_prod__financing"
            ),
            monthly_plan_sum_month=self.sum_month_by_param(
                year, month, "yearly__monthly_prod__monthly_plan_money"
            ),
            monthly_financing_sum_month=self.sum_month_by_param(
                year, month, "yearly__monthly_prod__financing"
            ),
            production_money_month=self.sum_month_by_param(
                year, month, "yearly__monthly_prod__base_prod__money_amount"
            ),
        )

    def get_pto_republic_stat_total(self, year, month):
        return self.aggregate(
            yearly_plan_money=Sum(
                Coalesce(
                    Case(
                        When(
                            Q(yearly__year__year=year),
                            then="yearly__money_amount_plan",
                        )
                    ),
                    0,
                ),
                distinct=True,
            ),
            production_money_until_month=self.sum_month_lte_by_param(
                year, month, "yearly__monthly_prod__base_prod__money_amount"
            ),
            monthly_plan_sum_until_month=self.sum_month_lte_by_param(
                year, month, "yearly__monthly_prod__monthly_plan_money"
            ),
            monthly_financing_sum_until_month=self.sum_month_lte_by_param(
                year, month, "yearly__monthly_prod__financing"
            ),
            monthly_financing_sum_month=self.sum_month_by_param(
                year, month, "yearly__monthly_prod__financing"
            ),
            production_money_month=self.sum_month_by_param(
                year, month, "yearly__monthly_prod__base_prod__money_amount"
            ),
            monthly_plan_sum_month=self.sum_month_by_param(
                year, month, "yearly__monthly_prod__monthly_plan_money"
            ),
        )

    def get_pto_republic_stat_sum(self, year, month):
        return (
            self.values("road_type")
            .annotate_statistics(year, month)
            .order_by("road_type")
        )

    def get_pto_republic_stat(self, year, month):
        return (
            self.values("road_type", "yearly__organization")
            .annotate_statistics(year, month)
            .filter(yearly_plan_money__gt=0)
        ).order_by("road_type")


class RoadManager(models.Manager):
    def get_queryset(self):
        return RoadQuerySet(model=self.model, using=self._db)

    def get_pto_republic_stat(self, year, month):
        return self.get_queryset().get_pto_republic_stat(
            year=year, month=month
        )

    def get_pto_republic_stat_sum(self, year, month):
        return self.get_queryset().get_pto_republic_stat_sum(
            year=year, month=month
        )

    def get_pto_republic_stat_total(self, year, month):
        return self.get_queryset().get_pto_republic_stat_total(year, month)


class Road(BaseModel):
    class RoadType(models.IntegerChoices):
        INTERNATIONAL = 1, _("Халқаро")
        GOVERNMENT = 2, _("Давлат")
        LOCAL = 3, _("Маҳаллий")

    title = models.CharField(max_length=512)
    code = models.CharField(max_length=10)
    district = models.ManyToManyField(
        "District",
        through="RoadDistrict",
        through_fields=("road", "district"),
        related_name="roads",
    )
    road_type = models.IntegerField(choices=RoadType.choices)
    search_vector = SearchVectorField(blank=True, null=True)
    objects = RoadManager()

    class Meta:
        verbose_name = _("Road")
        verbose_name_plural = _("Roads")
        indexes = [
            models.Index(fields=["code", "title"]),
            GinIndex(fields=["search_vector"]),
            BrinIndex(fields=["created_at"]),
        ]

    def __str__(self):
        return f"{self.code} {self.title} "


def plant_quantity_by_road_type(road_type):
    return Coalesce(
        Sum(
            Case(
                When(
                    Q(road__road_type=road_type),
                    then="plantedplants__quantity",
                ),
                default=Value("0"),
            )
        ),
        0,
    )


def quantity_by_road_and_plant_type(plant_type, road_type):
    return Coalesce(
        Sum(
            Case(
                When(
                    Q(road__road_type=road_type)
                    & Q(plantedplants__plant__type=plant_type),
                    then=F("plantedplants__quantity"),
                ),
                default=Value("0"),
            )
        ),
        0,
    )


def quantity_by_plant_type(plant_type):
    return Coalesce(
        Sum(
            Case(
                When(
                    plantedplants__plant__type=plant_type,
                    then=F("plantedplants__quantity"),
                ),
                default=Value("0"),
            )
        ),
        0,
    )


def planted_plant_road_length(road_type):
    return Coalesce(
        Sum(
            Case(
                When(
                    Q(road__road_type=road_type),
                    then='plantedplants__metr',
                    # then=F("plantedplants__road_to")
                    # - F("plantedplants__road_from"),
                ),
                default=Value("0"),
            )
        ),
        0,
    )


class RoadDistrictQuerySet(models.QuerySet):
    def annotate_stat_by_road_type_and_plant_type(self):
        return self.annotate(
            international_sum=plant_quantity_by_road_type(
                Road.RoadType.INTERNATIONAL
            ),
            international_len_sum=planted_plant_road_length(
                Road.RoadType.INTERNATIONAL
            ),
            international_bush_sum=quantity_by_road_and_plant_type(
                Plant.PlantType.BUSH, Road.RoadType.INTERNATIONAL
            ),
            international_leafy_shaped_sum=quantity_by_road_and_plant_type(
                Plant.PlantType.LEAF_SHAPED, Road.RoadType.INTERNATIONAL
            ),
            international_coniferous_shaped_sum=(
                quantity_by_road_and_plant_type(
                    Plant.PlantType.CONIFEROUS, Road.RoadType.INTERNATIONAL
                )
            ),
            government_sum=plant_quantity_by_road_type(
                Road.RoadType.GOVERNMENT
            ),
            government_len_sum=planted_plant_road_length(
                Road.RoadType.GOVERNMENT
            ),
            government_bush_sum=quantity_by_road_and_plant_type(
                Plant.PlantType.BUSH, Road.RoadType.GOVERNMENT
            ),
            government_leafy_shaped_sum=quantity_by_road_and_plant_type(
                Plant.PlantType.LEAF_SHAPED, Road.RoadType.GOVERNMENT
            ),
            government_coniferous_shaped_sum=quantity_by_road_and_plant_type(
                Plant.PlantType.CONIFEROUS, Road.RoadType.GOVERNMENT
            ),
            local_sum=plant_quantity_by_road_type(Road.RoadType.LOCAL),
            local_len_sum=planted_plant_road_length(Road.RoadType.LOCAL),
            local_bush_sum=quantity_by_road_and_plant_type(
                Plant.PlantType.BUSH, Road.RoadType.LOCAL
            ),
            local_leafy_shaped_sum=quantity_by_road_and_plant_type(
                Plant.PlantType.LEAF_SHAPED, Road.RoadType.LOCAL
            ),
            local_coniferous_shaped_sum=quantity_by_road_and_plant_type(
                Plant.PlantType.CONIFEROUS, Road.RoadType.LOCAL
            ),
            all_sum=F("international_sum")
            + F("government_sum")
            + F("local_sum"),
            all_len_sum=F("international_len_sum")
            + F("government_len_sum")
            + F("local_len_sum"),
            all_bush_sum=F("international_bush_sum")
            + F("government_bush_sum")
            + F("local_bush_sum"),
            all_leafy_shaped_sum=F("international_leafy_shaped_sum")
            + F("government_leafy_shaped_sum")
            + F("local_leafy_shaped_sum"),
            all_coniferous_shaped_sum=F("international_coniferous_shaped_sum")
            + F("government_coniferous_shaped_sum")
            + F("local_coniferous_shaped_sum"),
        )

    def get_plantedplants_quantity_by_district(self, district_id):
        return (
            self.values("district__name")
            .annotate_stat_by_road_type_and_plant_type()
            .filter(district__id=district_id)
        )

    def get_plantedplants_quantity_by_region(self, region_id):
        return (
            self.values("district__region__name")
            .annotate_stat_by_road_type_and_plant_type()
            .filter(district__region__id=region_id)
        )

    def get_plantedplants_quantity_republic(self):
        return self.aggregate(
            international_sum=plant_quantity_by_road_type(
                Road.RoadType.INTERNATIONAL
            ),
            international_len_sum=planted_plant_road_length(
                Road.RoadType.INTERNATIONAL
            ),
            international_bush_sum=quantity_by_road_and_plant_type(
                Plant.PlantType.BUSH, Road.RoadType.INTERNATIONAL
            ),
            international_leafy_shaped_sum=quantity_by_road_and_plant_type(
                Plant.PlantType.LEAF_SHAPED, Road.RoadType.INTERNATIONAL
            ),
            international_coniferous_shaped_sum=(
                quantity_by_road_and_plant_type(
                    Plant.PlantType.CONIFEROUS, Road.RoadType.INTERNATIONAL
                )
            ),
            government_sum=plant_quantity_by_road_type(
                Road.RoadType.GOVERNMENT
            ),
            government_len_sum=planted_plant_road_length(
                Road.RoadType.GOVERNMENT
            ),
            government_bush_sum=quantity_by_road_and_plant_type(
                Plant.PlantType.BUSH, Road.RoadType.GOVERNMENT
            ),
            government_leafy_shaped_sum=quantity_by_road_and_plant_type(
                Plant.PlantType.LEAF_SHAPED, Road.RoadType.GOVERNMENT
            ),
            government_coniferous_shaped_sum=quantity_by_road_and_plant_type(
                Plant.PlantType.CONIFEROUS, Road.RoadType.GOVERNMENT
            ),
            local_sum=plant_quantity_by_road_type(Road.RoadType.LOCAL),
            local_len_sum=planted_plant_road_length(Road.RoadType.LOCAL),
            local_bush_sum=quantity_by_road_and_plant_type(
                Plant.PlantType.BUSH, Road.RoadType.LOCAL
            ),
            local_leafy_shaped_sum=quantity_by_road_and_plant_type(
                Plant.PlantType.LEAF_SHAPED, Road.RoadType.LOCAL
            ),
            local_coniferous_shaped_sum=quantity_by_road_and_plant_type(
                Plant.PlantType.CONIFEROUS, Road.RoadType.LOCAL
            ),
            all_sum=Coalesce(Sum("plantedplants__quantity"), 0),
            all_len_sum=Coalesce(
                Sum(
                    F("plantedplants__road_to") - F("plantedplants__road_from")
                ),
                0,
            ),
            all_bush_sum=quantity_by_plant_type(Plant.PlantType.BUSH),
            all_leafy_shaped_sum=quantity_by_plant_type(
                Plant.PlantType.LEAF_SHAPED
            ),
            all_coniferous_shaped_sum=quantity_by_plant_type(
                Plant.PlantType.CONIFEROUS
            ),
        )

    def get_plantedplants_quantity_region(self, region):
        return self.filter(district__region=region).get_all_statistics()

    def filter_by_district(self, district_id):
        return self.select_related("road").filter(district_id=district_id)

    def sum_quantity_by_type(self, plant_type):
        return Sum(
            Case(
                When(
                    plantedplants__plant__type=plant_type,
                    then="plantedplants__quantity",
                ),
                default=Value("0"),
            )
        )

    def get_planted_plants(self, region):
        return (
            self.select_related("road", "district")
            .annotate(
                total_quantity=Coalesce(Sum("plantedplants__quantity"), 0),
                leafy=self.sum_quantity_by_type(Plant.PlantType.LEAF_SHAPED),
                nail_leaf=self.sum_quantity_by_type(
                    Plant.PlantType.CONIFEROUS
                ),
                bushes=self.sum_quantity_by_type(Plant.PlantType.BUSH),
                planted_road=Coalesce(
                    Sum(
                        F("plantedplants__road_to")
                        - F("plantedplants__road_from")
                    ),
                    0,
                ),
            )
            .filter(district__region=region)
            .order_by("district__name", "road__road_type")
        )

    def get_by_road_type(self, region):
        result = (
            self.select_related("road")
            .values("road__road_type", "district__region__name")
            .annotate(
                total_quantity=Coalesce(Sum("plantedplants__quantity"), 0),
                leafy=self.sum_quantity_by_type(Plant.PlantType.LEAF_SHAPED),
                nail_leaf=self.sum_quantity_by_type(
                    Plant.PlantType.CONIFEROUS
                ),
                bushes=self.sum_quantity_by_type(Plant.PlantType.BUSH),
                planted_road=Coalesce(
                    # Sum(
                    #     F("plantedplants__road_to")
                    #     - F("plantedplants__road_from")
                    # ),
                    Sum(
                        'plantedplants__metr'
                    ),
                    0,
                ),
                requirements=Sum("requirement"),
                road_slice=Sum(F("road_to") - F("road_from")),
            )
            .filter(district__region=region)
            .order_by("road__road_type")
        )

        return result

    def get_by_region(self):
        result = (
            self.select_related("road")
            .values("district__region__id", "road__road_type")
            .annotate(
                total_quantity=Coalesce(Sum("plantedplants__quantity"), 0),
                leafy=self.sum_quantity_by_type(Plant.PlantType.LEAF_SHAPED),
                nail_leaf=self.sum_quantity_by_type(
                    Plant.PlantType.CONIFEROUS
                ),
                bushes=self.sum_quantity_by_type(Plant.PlantType.BUSH),
                planted_road=Coalesce(
                    # Sum(
                    #     F("plantedplants__road_to")
                    #     - F("plantedplants__road_from")
                    # ),
                    Sum(
                        'plantedplants__metr'
                    ),
                    0,
                ),
                requirements=Sum("requirement"),
                road_slice=Sum(F("road_to") - F("road_from")),
            )
            .order_by("district__region__name", "road__road_type")
        )
        return result

    def get_republic_stat_by_road_type(self):
        result = (
            self.select_related("road")
            .values("road__road_type")
            .annotate(
                total_quantity=Coalesce(Sum("plantedplants__quantity"), 0),
                leafy=self.sum_quantity_by_type(Plant.PlantType.LEAF_SHAPED),
                nail_leaf=self.sum_quantity_by_type(
                    Plant.PlantType.CONIFEROUS
                ),
                bushes=self.sum_quantity_by_type(Plant.PlantType.BUSH),
                planted_road=Coalesce(
                    # Sum(
                    #     F("plantedplants__road_to")
                    #     - F("plantedplants__road_from")
                    # ),
                    Sum(
                        'plantedplants__metr'
                    ),
                    0,
                ),
                requirements=Sum("requirement"),
                road_slice=Sum(F("road_to") - F("road_from")),
            )
            .order_by("road__road_type")
        )
        return result

    def get_road_district(self):
        return self.select_related("road", "district").order_by("-requirement")

    def get_all_statistics(self):
        return self.values("road__road_type").aggregate(
            total_quantity=Coalesce(Sum("plantedplants__quantity"), 0),
            leafy=self.sum_quantity_by_type(Plant.PlantType.LEAF_SHAPED),
            nail_leaf=self.sum_quantity_by_type(Plant.PlantType.CONIFEROUS),
            bushes=self.sum_quantity_by_type(Plant.PlantType.BUSH),
            planted_road=Coalesce(
                # Sum(
                #     F("plantedplants__road_to") - F("plantedplants__road_from")
                # ),
                Sum(
                    'plantedplants__metr'
                ),
                0,
            ),
            requirements=Sum("requirement"),
            road_slice=Sum(F("road_to") - F("road_from")),
        )

    def get_regions_total_stat(self):
        result = (
            self.select_related("road")
            .values(
                region_name=F("district__region__name"),
                region_id=F("district__region__id"),
            )
            .annotate(
                total_quantity=Coalesce(Sum("plantedplants__quantity"), 0),
                leafy=self.sum_quantity_by_type(Plant.PlantType.LEAF_SHAPED),
                nail_leaf=self.sum_quantity_by_type(
                    Plant.PlantType.CONIFEROUS
                ),
                bushes=self.sum_quantity_by_type(Plant.PlantType.BUSH),
                planted_road=Coalesce(
                    # Sum(
                    #     F("plantedplants__road_to")
                    #     - F("plantedplants__road_from")
                    # ),
                    Sum(
                        'plantedplants__metr'
                    ),
                    0,
                ),
                requirements=Sum("requirement"),
                road_slice=Sum(F("road_to") - F("road_from")),
            )
            .order_by("district__region__id")
        )
        return result


class RoadDistrictManager(models.Manager):
    def get_queryset(self):
        return RoadDistrictQuerySet(model=self.model, using=self._db)

    def get_plantedplants_quantity_by_district(self, district_id):
        return self.get_queryset().get_plantedplants_quantity_by_district(
            district_id
        )

    def get_plantedplants_quantity_by_region(self, region_id):
        return self.get_queryset().get_plantedplants_quantity_by_region(
            region_id
        )

    def filter_by_district(self, district_id):
        return self.get_queryset().filter_by_district(district_id)

    def get_planted_plants(self, region):
        return self.get_queryset().get_planted_plants(region)

    def get_by_road_type(self, region):
        return self.get_queryset().get_by_road_type(region)

    def get_by_region(self):
        return self.get_queryset().get_by_region()

    def get_road_district(self):
        return self.get_queryset().get_road_district()

    def get_all_statistics(self):
        return self.get_queryset().get_all_statistics()

    def get_plantedplants_quantity_republic(self):
        return self.get_queryset().get_plantedplants_quantity_republic()

    def get_republic_stat_by_road_type(self):
        return self.get_queryset().get_republic_stat_by_road_type()

    def get_plantedplants_quantity_region(self, region):
        return self.get_queryset().get_plantedplants_quantity_region(region)

    def get_regions_total_stat(self):
        return self.get_queryset().get_regions_total_stat()


class RoadDistrict(BaseModel):
    road = models.ForeignKey(Road, on_delete=models.CASCADE)
    district = models.ForeignKey(District, on_delete=models.CASCADE)
    road_from = models.FloatField()
    road_to = models.FloatField()
    requirement = models.FloatField()
    objects = RoadDistrictManager()

    def __str__(self):
        return self.road.title

    class Meta:
        unique_together = ("road", "district")
