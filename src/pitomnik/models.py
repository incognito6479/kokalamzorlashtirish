import datetime
from datetime import date

from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import (
    Case,
    Count,
    DecimalField,
    F,
    IntegerField,
    OuterRef,
    Q,
    Subquery,
    Sum,
    Value,
    When,
)
from django.db.models.functions import Coalesce
from django.utils.translation import gettext_lazy as _

from common.models import BaseModel


class PlantQuerySet(models.QuerySet):
    def get_plants(self):
        return self.values(plant_id=F("id"), plant_name=F("name"))


class PlantManager(models.Manager):
    def get_queryset(self):
        return PlantQuerySet(self.model, using=self._db)

    def get_plants(self):
        return self.get_queryset().get_plants()


class Plant(BaseModel):
    class PlantType(models.TextChoices):
        LEAF_SHAPED = "LEAF_SHAPED", _("Япрок баргли")
        CONIFEROUS = "CONIFEROUS", _("Игна Баргли")
        BUSH = "BUSH", _("Бута")

    name = models.CharField(max_length=255, blank=False, null=False)
    type = models.CharField(choices=PlantType.choices, max_length=15)
    objects = PlantManager()
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f"{self.name}"


class PitomnikManager(models.Manager):
    def filter_by_organization(self, organization):
        return self.get_queryset().filter(organization=organization)

    def filter_by_organization_or_all(self, user):
        print(user.organization)
        if user.organization.name == "УП Ўзйулкукаламзорлаштириш":
            return self.get_queryset().all()
        return self.get_queryset().filter(organization=user.organization)

    def pitomnik_for_excel(self):
        return (
            self.values("name")
            .annotate(
                total_quantity=Coalesce(Sum("pitomnikplants__quantity"), 0),
                sprout_quantity=Sum(
                    Case(
                        When(
                            pitomnikplants__plant_type=(
                                PitomnikPlants.PlantType.SPROUT
                            ),
                            then="pitomnikplants__quantity",
                        ),
                        default=0,
                    )
                ),
                seed_quantity=Sum(
                    Case(
                        When(
                            pitomnikplants__plant_type=(
                                PitomnikPlants.PlantType.SEED
                            ),
                            then="pitomnikplants__quantity",
                        ),
                        default=0,
                    )
                ),
                ready_quantity=Sum(
                    Case(
                        When(
                            pitomnikplants__readiness_date__lte=date.today(),
                            then="pitomnikplants__quantity",
                        ),
                        default=0,
                    )
                ),
            )
            .values(
                "name",
                "area",
                "total_quantity",
                "seed_quantity",
                "sprout_quantity",
                "ready_quantity",
            )
        )


class Pitomnik(BaseModel):
    name = models.CharField(max_length=255, blank=False, null=False)
    address = models.TextField()
    kontr = models.CharField(max_length=255, blank=False, null=False)
    area = models.FloatField()
    plants = models.ManyToManyField(
        Plant, through="PitomnikPlants", related_name="pitomnik"
    )
    objects = PitomnikManager()
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    organization = models.ForeignKey(
        "account.Organization", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.name}"

    def get_all_plant_count(self):
        return self.plants.count()

    class Meta:
        ordering = ("-id",)

    @property
    def has_image(self):
        if self.images.count():
            return True
        return False


class PitomnikPlantsQuerySet(models.QuerySet):
    def get_plants_by_organization(self, organization):
        base_queryset = self.select_related(
            "pitomnik", "plant"
        ).prefetch_related("images")
        base_queryset = base_queryset.filter(
            action_type=PitomnikPlants.ActionTYPE.IMPORT
        )
        base_queryset = base_queryset.filter(
            pitomnik__organization=organization
        )
        return base_queryset

    def get_plants_by_pitomnik(self, pitomnik_id):
        return (
            self.values("plant_id", plant_name=F("plant__name"))
            .annotate(
                total_quantity=Sum(
                    Case(
                        When(
                            Q(readiness_date__isnull=True)
                            | Q(readiness_date__lte=date.today()),
                            then="quantity",
                        ),
                        default=Value(0),
                        output_field=IntegerField(),
                    ),
                )
            )
            .filter(pitomnik_id=pitomnik_id, total_quantity__gt=0)
            .order_by("plant")
        )

    def get_plant_total_quantity(self, pitomnik, plant):
        return (
            self.values("pitomnik", "plant")
            .annotate(total_quantity=Sum("quantity"))
            .get(pitomnik=pitomnik, plant=plant)
        )


class PitomnikPlantsManager(models.Manager):
    def get_queryset(self):
        return PitomnikPlantsQuerySet(self.model, using=self._db)

    def get_plants_by_organization(self, organization):
        return self.get_queryset().get_plants_by_organization(organization)

    def pitomnik_plant_stats(
        self, organization, plant_type=None, pitomnik=None
    ):
        output = DecimalField(max_digits=20, decimal_places=2)
        plants = Plant.objects.all()
        readiness_date = date.today()

        plant_types = dict(
            bush="BUSH",
            leaf_shaped_tree="LEAF_SHAPED",
            coniferous_tree="CONIFEROUS",
        )

        base_queryset = self
        if organization:
            base_queryset = base_queryset.filter(
                pitomnik__organization_id=organization
            )

        if plant_type in plant_types.keys():
            plant_type = plant_types.get(plant_type, None)
            plants = plants.filter(type=plant_type)

        if pitomnik:
            base_queryset = base_queryset.filter(pitomnik=pitomnik)

        base_queryset = base_queryset.filter(plant=OuterRef("pk"))

        queryset_quantity = base_queryset.order_by()
        queryset_quantity = queryset_quantity.annotate(
            all_quantity=Sum("quantity")
        )
        queryset_quantity = queryset_quantity.values("all_quantity")
        queryset_quantity.query.group_by = []

        queryset_plant_field = base_queryset.order_by()
        queryset_plant_field = queryset_plant_field.annotate(
            all_field=Sum("plant_field")
        )
        queryset_plant_field = queryset_plant_field.values("all_field")
        queryset_plant_field.query.group_by = []

        base_queryset = base_queryset.filter(
            Q(readiness_date__lte=readiness_date)
            | Q(readiness_date__isnull=True)
        )

        queryset_read_plant = base_queryset.order_by()
        queryset_read_plant = queryset_read_plant.annotate(
            ready_quantity=Coalesce(Sum("quantity"), 0)
        )
        queryset_read_plant = queryset_read_plant.values("ready_quantity")
        queryset_read_plant.query.group_by = []

        plants = plants.annotate(
            total_plant_quantity=Subquery(
                queryset_quantity[:1], output_field=output
            )
        )
        plants = plants.annotate(
            ready_plant_quantity=Subquery(
                queryset_read_plant[:1], output_field=output
            )
        )
        plants = plants.annotate(
            field_to_be_planted=Subquery(
                queryset_plant_field[:1], output_field=output
            )
        )
        plants = plants.exclude(total_plant_quantity__isnull=True)
        plants = plants.values(
            "name",
            "total_plant_quantity",
            "ready_plant_quantity",
            "field_to_be_planted",
        )
        plants = plants.order_by("-total_plant_quantity")
        return plants

    def get_total_statistics(self, organization, plant_type):
        arr = []
        query = self.pitomnik_plant_stats(organization, plant_type)
        arr.append(
            query.aggregate(
                total_plant=Coalesce(Sum("total_plant_quantity"), 0)
            )
        )
        arr.append(
            query.aggregate(
                total_ready_plant=Coalesce(Sum("ready_plant_quantity"), 0)
            )
        )
        arr.append(
            query.aggregate(
                total_field_to_be_planted=Coalesce(
                    Sum("field_to_be_planted"), 0
                )
            )
        )

        return arr

    def get_plants(self, pitomnik_id=None):
        if pitomnik_id:
            return self.get_queryset().get_plants_by_pitomnik(pitomnik_id)
        return Plant.objects.get_plants()

    def get_plant_total_quantity(self, pitomnik, plant):
        return self.get_queryset().get_plant_total_quantity(pitomnik, plant)

    def create_export(self, pitomnik, plant, quantity, user):
        quantity = -(abs(quantity))
        self.create(
            pitomnik=pitomnik,
            plant=plant,
            quantity=quantity,
            plant_field=0,
            action_type=PitomnikPlants.ActionTYPE.EXPORT,
            added_by=user,
        )


    def create_import(self, pitomnik, plant, quantity, user):
        self.create(
            pitomnik=pitomnik,
            plant=plant,
            quantity=quantity,
            plant_field=0,
            action_type=PitomnikPlants.ActionTYPE.EXPORT,
            added_by=user,
        )
    def get_plant_and_pitomnik_and_organization(self):
        return (
            self.select_related("pitomnik", "pitomnik__organization", "plant")
            .prefetch_related("images")
            .filter(action_type=PitomnikPlants.ActionTYPE.IMPORT)
            .exclude(
                pitomnik__organization__name__in=[
                    "Admin",
                    "УП Ўзйулкукаламзорлаштириш",
                ]
            )
        )

    def get_pitomnik_plant_for_excel(self):
        # return self.values("pitomnik")
        return (
            self.select_related("pitomnik", "pitomnik__organization", "plant")
                .prefetch_related("images")
                .filter(action_type=PitomnikPlants.ActionTYPE.IMPORT)
                .exclude(
                pitomnik__organization__name__in=[
                    "Admin",
                    "УП Ўзйулкукаламзорлаштириш",
                ]
            )
        )

class PitomnikPlants(BaseModel):
    class PlantType(models.TextChoices):
        SPROUT = "SPROUT", _("Ниҳолдан")
        SEED = "SEED", _("Уруғдан")

    class ActionTYPE(models.TextChoices):
        IMPORT = "Import", _("Import")
        EXPORT = "Export", _("Export")

    pitomnik = models.ForeignKey(Pitomnik, on_delete=models.CASCADE)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    plant_type = models.CharField(
        choices=PlantType.choices, max_length=10, blank=True
    )
    plant_field = models.DecimalField(
        max_digits=20, decimal_places=2, default=0
    )
    planted_date = models.DateField(default=datetime.date.today)
    readiness_date = models.DateField(null=True, blank=True)
    action_type = models.CharField(
        max_length=10, choices=ActionTYPE.choices, default=ActionTYPE.IMPORT
    )
    dried = models.PositiveIntegerField(default=0)
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    objects = PitomnikPlantsManager()

    class Meta:
        verbose_name_plural = "Pitomnik Plants"
        ordering = ("-created_at",)

    @property
    def has_image(self):
        if self.images.count():
            return True
        return False


class PitomnikPlantImageManager(models.Manager):
    def filter_by_pitomnik_plant(self, pitomnik_plant_id, user):
        queryset = self.select_related("pitomnik_plant").filter(
            pitomnik_plant_id=pitomnik_plant_id
        )
        if not user.has_perm("pitomnik.view_pitomnik_admin"):
            queryset = queryset.filter(
                pitomnik_plant__pitomnik__organization=user.organization
            )
        return queryset


class PitomnikPlantImage(BaseModel):
    image = models.ImageField(upload_to="pitomnikplant_images/%Y/%m/%d/")
    pitomnik_plant = models.ForeignKey(
        PitomnikPlants, on_delete=models.CASCADE, related_name="images"
    )
    objects = PitomnikPlantImageManager()


class PlantedPlantsQuerySet(models.QuerySet):
    def get_planted_plants(self, organization):
        return (
            self.select_related(
                "road_district__road",
                "road_district__district",
                "pitomnik",
                "plant",
            )
            .prefetch_related("images")
            .filter(added_by__organization=organization)
            .order_by("-created_at")
        )


class PlantedPlantsManager(models.Manager):
    def get_queryset(self):
        return PlantedPlantsQuerySet(self.model, using=self._db)

    def get_planted_plants(self, organization):
        return self.get_queryset().get_planted_plants(organization)

    def get_quantity_plant(self, organization):
        return (
            self.select_related(
                "plant",
            )
            .filter(added_by__organization=organization)
            .values("plant__name")
            .annotate(plant_quantity=Coalesce(Sum("quantity"), 0))
        )

    def get_total_quantity_by_organization(self, organization):
        return (
            self.select_related(
                "plant",
            )
            .filter(added_by__organization=organization)
            .aggregate(
                total_sum=Coalesce(Sum("quantity"), 0),
                road_slice=(Coalesce((Sum("road_to") - Sum("road_from")), 0)),
            )
        )


class PlantedPlants(BaseModel):
    class SourceType(models.TextChoices):
        PITOMNIK = "PITOMNIK", _("Питомникдан")
        FOREST = "FOREST", _("Ўрмондан")
        OTHERS = "OTHERS", _("Бошқа")

    class PlantingSide(models.TextChoices):
        RIGHT = "RIGHT", _("Ўнг тараф")
        LEFT = "LEFT", _("Чап тараф")
        BOTH = "BOTH", _("Ўнг ва Чап тараф")

    plant_source = models.CharField(
        "Манба",
        choices=SourceType.choices,
        max_length=15,
        default=SourceType.OTHERS,
    )
    planting_side = models.CharField(
        choices=PlantingSide.choices, max_length=5
    )
    pitomnik = models.ForeignKey(Pitomnik, on_delete=models.CASCADE, null=True)
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    road_district = models.ForeignKey(
        "regionroad.RoadDistrict", on_delete=models.CASCADE
    )
    road_from = models.FloatField()
    road_to = models.FloatField()
    planted_date = models.DateField(default=datetime.date.today)
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    metr = models.IntegerField(null=True)
    district = models.ForeignKey("regionroad.District", on_delete=models.CASCADE, null=True)
    objects = PlantedPlantsManager()

    class Meta:
        verbose_name = "Planted Plant"
        verbose_name_plural = "Planted Plants"

    @property
    def has_image(self):
        if self.images.count():
            return True
        return False

    def delete(self, using=None, keep_parents=False):
        if self.pitomnik:
            pitomnik_plant = PitomnikPlants.objects.filter(
                pitomnik=self.pitomnik,
                plant=self.plant,
                quantity=-self.quantity,
                action_type=PitomnikPlants.ActionTYPE.EXPORT,
                created_at__date=self.created_at,
            ).first()
            if pitomnik_plant:
                pitomnik_plant.delete()
        return super().delete()


class PitomnikImageManager(models.Manager):
    def filter_by_pitomnik(self, pitomnik_id, user):
        queryset = self.select_related("pitomnik").filter(
            pitomnik_id=pitomnik_id
        )
        if not user.has_perm("pitomnik.view_pitomnik_admin"):
            queryset = queryset.filter(
                pitomnik__organization=user.organization
            )
        return queryset


class PitomnikImage(BaseModel):
    image = models.ImageField(upload_to="pitomnik_images/%Y/%m/%d/")
    pitomnik = models.ForeignKey(
        Pitomnik, on_delete=models.CASCADE, related_name="images"
    )
    objects = PitomnikImageManager()


class PlantedPlantImageManager(models.Manager):
    def filter_by_planted_plant(self, planted_plant_id):
        return self.select_related(
            "planted_plant__road_district__road"
        ).filter(planted_plant_id=planted_plant_id)


class PlantedPlantImage(BaseModel):
    image = models.ImageField(upload_to="planted_plant_images/%Y/%m/%d/")
    planted_plant = models.ForeignKey(
        PlantedPlants, on_delete=models.CASCADE, related_name="images"
    )
    objects = PlantedPlantImageManager()


class LandScapeJobQuerySet(models.QuerySet):
    def filter_by_organization(self, organization):
        return (
            self.filter(organization=organization)
            .select_related("road_district__road")
            .prefetch_related("images")
            .order_by("-created_at")
        )

    def aggregate_total(self):
        return self.values("organization__name", "organization__id").annotate(
            total_round_quantity=Sum("round_quantity"),
            total_round_area=Sum("round_area"),
            total_cross_quantity=Sum("cross_quantity"),
            total_cross_area=Sum("cross_area"),
            total_panno_quantity=Sum("panno_quantity"),
            total_road_side_length=Sum("road_side_length"),
        )


class LandScapeJobManager(models.Manager):
    def get_queryset(self):
        return LandScapeJobQuerySet(model=self.model, using=self._db)

    def filter_by_organization(self, organization):
        return self.get_queryset().filter_by_organization(organization)

    def filter_by_organization_admin(self, organization):
        return self.get_queryset().filter_by_organization(organization)

    def aggregate_total(self):
        return self.get_queryset().aggregate_total()


class LandScapeJob(BaseModel):
    road_district = models.ForeignKey(
        "regionroad.RoadDistrict", on_delete=models.CASCADE
    )
    road_slice = ArrayField(models.FloatField())
    round_quantity = models.IntegerField()
    round_area = models.FloatField()
    cross_quantity = models.IntegerField()
    cross_area = models.FloatField()
    panno_quantity = models.IntegerField()
    road_side_length = models.FloatField()
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    organization = models.ForeignKey(
        "account.Organization", on_delete=models.CASCADE
    )
    objects = LandScapeJobManager()

    def __str__(self):
        return self.road.title

    @property
    def has_image(self):
        if self.images.count():
            return True
        return False


class IrrigationQuerySet(models.QuerySet):
    def get_irrigation_by_organization(self, organization):
        return (
            self.filter(organization=organization)
            .select_related("road_district__road")
            .prefetch_related("images")
            .order_by("-created_at")
        )

    def _sum_quantity_by_type(self, irrigation_type):
        return Sum(
            Case(
                When(
                    irrigation_type=irrigation_type,
                    then="tree_quantity",
                ),
                default=Value("0"),
            )
        )

    def _sum_len_by_type(self, irrigation_type):
        return Sum(
            Case(
                When(irrigation_type=irrigation_type, then="length"),
                default=Value("0"),
            )
        )

    def get_irrigation_list_for_admin(self):
        queryset = (
            self.values("organization__id", "organization__name")
            .annotate(
                streams_quantity=self._sum_quantity_by_type(
                    IrrigationType.STREAMS
                ),
                by_car_quantity=self._sum_quantity_by_type(
                    IrrigationType.BY_CAR
                ),
                pum_and_motor_quantity=self._sum_quantity_by_type(
                    IrrigationType.PUMP_AND_MOTOR
                ),
                drip_and_rain_quantity=self._sum_quantity_by_type(
                    IrrigationType.DRIP_AND_RAIN
                ),
                streams_len=self._sum_quantity_by_type(IrrigationType.STREAMS),
                by_car_len=self._sum_len_by_type(IrrigationType.BY_CAR),
                pum_and_len=self._sum_len_by_type(
                    IrrigationType.PUMP_AND_MOTOR
                ),
                drip_and_rain_len=self._sum_len_by_type(
                    IrrigationType.DRIP_AND_RAIN
                ),
            )
            .order_by("-organization__id")
        )
        return queryset

    def get_irrigation_count_local(self, user):
        return (
            self.values("irrigation_type")
            .annotate(irrigation_count=Count("id"))
            .filter(organization=user.organization)
            .order_by("irrigation_type")
        )

    def get_irrigation_count_admin(self):
        return (
            self.values("irrigation_type")
            .annotate(irrigation_count=Count("id"))
            .order_by("irrigation_type")
        )


class IrrigationManager(models.Manager):
    def get_queryset(self):
        return IrrigationQuerySet(model=self.model, using=self._db)

    def get_irrigation_count_local(self, user):
        return self.get_queryset().get_irrigation_count_local(user)

    def get_irrigation_count_admin(self):
        return self.get_queryset().get_irrigation_count_admin()

    def get_irrigation_by_organization(self, organization):
        return self.get_queryset().get_irrigation_by_organization(organization)

    def get_irrigation_list_for_admin(self):
        return self.get_queryset().get_irrigation_list_for_admin()


class IrrigationType(models.TextChoices):
    STREAMS = "STREAMS", _("Ариқлар ва қувурлар орқали")
    BY_CAR = "BY_CAR", _("Автотранспортда")
    PUMP_AND_MOTOR = "PUMP_AND_MOTOR", _("Насос ва мотопомпалар")
    DRIP_AND_RAIN = "DRIP_AND_RAIN", _("Томчилатиб, ёмғирлатиб")


class Irrigation(BaseModel):
    road_district = models.ForeignKey(
        "regionroad.RoadDistrict", on_delete=models.CASCADE
    )
    irrigation_type = models.CharField(
        choices=IrrigationType.choices, max_length=60
    )
    road_slice = ArrayField(models.FloatField())
    tree_quantity = models.IntegerField()
    length = models.FloatField()
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    organization = models.ForeignKey(
        "account.Organization", on_delete=models.CASCADE
    )
    objects = IrrigationManager()

    def __str__(self):
        return self.road_district.road.title

    @property
    def has_image(self):
        if self.images.count():
            return True
        return False


class SavingJobQuerySet(models.QuerySet):
    def filter_by_organization(self, organization):
        return (
            self.select_related(
                "road_district",
                "road_district__road",
                "road_district__district",
                "organization",
            )
            .prefetch_related("images")
            .filter(organization=organization)
            .annotate(
                tree_quantity=F("dig_quantity") + F("organic_quantity"),
                tree_len=F("organic_len") + F("dig_len"),
            )
            .order_by("-created_at")
        )

    def aggregate_quantity_len(self):
        return (
            self.values("organization__name", "organization__id")
            .annotate(
                dig_quantity=Sum("dig_quantity"),
                dig_len=Sum("dig_len"),
                organic_quantity=Sum("organic_quantity"),
                organic_len=Sum("organic_len"),
                workers_quantity=Sum("workers_quantity"),
                technique_quantity=Sum("technique_quantity"),
                tree_quantity_sum=F("dig_quantity") + F("organic_quantity"),
                tree_len_sum=F("organic_len") + F("dig_len"),
            )
            .order_by("organization__name")
        )


class SavingJobManager(models.Manager):
    def get_queryset(self):
        return SavingJobQuerySet(model=self.model, using=self._db)

    def filter_by_organization(self, user):
        return self.get_queryset().filter_by_organization(user.organization)

    def filter_by_organization_admin(self, organization):
        return self.get_queryset().filter_by_organization(organization)

    def aggregate_quantity_len(self):
        return self.get_queryset().aggregate_quantity_len()


class SavingJob(BaseModel):
    road_district = models.ForeignKey(
        "regionroad.RoadDistrict", on_delete=models.CASCADE
    )
    road_from = models.FloatField()
    road_to = models.FloatField()
    dig_quantity = models.IntegerField()
    dig_len = models.FloatField()
    organic_quantity = models.IntegerField()
    organic_len = models.FloatField()
    workers_quantity = models.IntegerField()
    technique_quantity = models.IntegerField()
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    organization = models.ForeignKey(
        "account.Organization", on_delete=models.CASCADE
    )
    objects = SavingJobManager()

    def __str__(self):
        return self.road_district.road.title

    @property
    def has_image(self):
        if self.images.count():
            return True
        return False


class NewIrrigationQuerySet(models.QuerySet):
    def filter_by_organization(self, organization):
        return (
            self.select_related(
                "road_district__road", "road_district__district"
            )
            .prefetch_related("images")
            .filter(organization=organization)
            .order_by("-created_at")
        )

    def aggregate_sum(self):
        return (
            self.values("organization__id", "organization__name")
            .annotate(
                total_artesian_well=Sum("artesian_well"),
                total_drop=Sum("drop"),
                total_rain=Sum("rain"),
            )
            .order_by("organization_id")
        )


class NewIrrigationManager(models.Manager):
    def get_queryset(self):
        return NewIrrigationQuerySet(model=self.model, using=self._db)

    def filter_by_organization(self, organization):
        return self.get_queryset().filter_by_organization(organization)

    def aggregate_sum(self):
        return self.get_queryset().aggregate_sum()


class NewIrrigation(BaseModel):
    road_district = models.ForeignKey(
        "regionroad.RoadDistrict", on_delete=models.CASCADE
    )
    road_from = models.FloatField()
    road_to = models.FloatField()
    artesian_well = models.PositiveIntegerField(default=0)
    drop = models.FloatField(default=0.0)
    rain = models.FloatField(default=0.0)
    added_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    organization = models.ForeignKey(
        "account.Organization", on_delete=models.CASCADE
    )
    objects = NewIrrigationManager()

    def __str__(self):
        return self.road_district.road.title

    @property
    def has_image(self):
        if self.images.count():
            return True
        return False


class PitomnikSavingJobQuerySet(models.QuerySet):
    def get_saving_job_organization(self, organization):
        base_queryset = self.select_related("pitomnik", "plants")
        base_queryset = base_queryset.filter(
            pitomnik__organization=organization
        ).order_by("-created_at")
        return base_queryset

    def group_by_plant_type(self, organization):
        result = (
            self.values("plants__type")
            .annotate(
                total_total_plants=Sum("total_plants"),
                total_planted_area=Sum("planted_area"),
                total_agrotechnical_measures=Sum("agrotechnical_measures"),
                total_mineral=Sum("mineral"),
                total_organic=Sum("organic"),
                total_workers=Sum("workers"),
                total_technique=Sum("technique"),
            )
            .filter(pitomnik__organization=organization)
        )
        return result


class PitomnikSavingJobManager(models.Manager):
    def get_queryset(self):
        return PitomnikSavingJobQuerySet(model=self.model, using=self._db)

    def group_by_plant_type(self, organization):
        return self.get_queryset().group_by_plant_type(organization)

    def get_saving_job_by_organization(self, organization):
        return self.get_queryset().get_saving_job_organization(organization)


class PitomnikSavingJob(BaseModel):
    pitomnik = models.ForeignKey(Pitomnik, on_delete=models.CASCADE)
    plants = models.ForeignKey(Plant, on_delete=models.CASCADE)
    total_plants = models.IntegerField(default=0)
    planted_area = models.FloatField(default=0)
    agrotechnical_measures = models.FloatField(default=0)
    mineral = models.FloatField(default=0)
    organic = models.FloatField(default=0)
    workers = models.IntegerField(default=0)
    technique = models.IntegerField(default=0)
    objects = PitomnikSavingJobManager()

    @property
    def has_image(self):
        if self.images.count():
            return True
        return False


class PitomnikSavingJobImageManager(models.Manager):
    def filter_by_pitomniksavingjob(self, pitomniksavingjob_id, user):
        queryset = self.select_related("pitomnik_saving_job").filter(
            pitomnik_saving_job_id=pitomniksavingjob_id
        )
        if not user.has_perm("pitomnik.view_pitomniksavingjob_admin"):
            queryset = queryset.filter(
                pitomniksavingjob__organization=user.organization
            )
        return queryset


class PitomnikSavingJobImage(BaseModel):
    image = models.ImageField(upload_to="pitomnik_saving_job/%Y/%m/%d/")
    pitomnik_saving_job = models.ForeignKey(
        PitomnikSavingJob, on_delete=models.CASCADE, related_name="images"
    )
    objects = PitomnikSavingJobImageManager()


class LandScapeJobImageManager(models.Manager):
    def filter_by_landscapejob(self, landscapejob_id, user):
        queryset = self.select_related("landscapejob").filter(
            landscapejob_id=landscapejob_id
        )
        if not user.has_perm("pitomnik.view_landscapejob_admin"):
            queryset = queryset.filter(
                landscapejob__organization=user.organization
            )
        return queryset


class LandScapeJobImage(BaseModel):
    image = models.ImageField(upload_to="landscapejob_images/%Y/%m/%d/")
    landscapejob = models.ForeignKey(
        LandScapeJob, on_delete=models.CASCADE, related_name="images"
    )
    objects = LandScapeJobImageManager()


class SavingjobImageManager(models.Manager):
    def filter_by_savingjob(self, savingjob_id, user):
        queryset = self.select_related("savingjob").filter(
            savingjob_id=savingjob_id
        )
        if not user.has_perm("pitomnik.view_savingjob_admin"):
            queryset = queryset.filter(
                savingjob__organization=user.organization
            )
        return queryset


class SavingjobImage(BaseModel):
    image = models.ImageField(upload_to="savingjob_images/%Y/%m/%d/")
    savingjob = models.ForeignKey(
        SavingJob, on_delete=models.CASCADE, related_name="images"
    )
    objects = SavingjobImageManager()


class IrrigationImageManager(models.Manager):
    def filter_by_irrigation(self, irrigation_id, user):
        queryset = self.select_related("irrigation").filter(
            irrigation_id=irrigation_id
        )
        if not user.has_perm("pitomnik.view_irrigation_admin"):
            queryset = queryset.filter(
                irrigation__organization=user.organization
            )
        return queryset


class IrrigationImage(BaseModel):
    image = models.ImageField(upload_to="irrigation_images/%Y/%m/%d/")
    irrigation = models.ForeignKey(
        Irrigation, on_delete=models.CASCADE, related_name="images"
    )
    objects = IrrigationImageManager()


class NewIrrigationImageManager(models.Manager):
    def filter_by_newirrigation(self, newirrigation_id, user):
        queryset = self.select_related("newirrigation").filter(
            newirrigation_id=newirrigation_id
        )
        if not user.has_perm("pitomnik.view_newirrigation_admin"):
            queryset = queryset.filter(
                newirrigation__organization=user.organization
            )
        return queryset


class NewIrrigationImage(BaseModel):
    image = models.ImageField(upload_to="newirrigation_images/%Y/%m/%d/")
    newirrigation = models.ForeignKey(
        NewIrrigation, on_delete=models.CASCADE, related_name="images"
    )
    objects = NewIrrigationImageManager()
