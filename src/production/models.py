from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import Case, F, Q, Subquery, Sum, When
from django.db.models.functions import Coalesce

from account.models import Organization, User
from common.models import BaseModel
from regionroad.models import Road


class YearlyProductionPlanQuerySet(models.QuerySet):
    def get_years_by_organization(self, user):
        return self.values_list("year__year").filter(
            organization=user.organization # road_address__len=2
        )

    def get_all(self):
        return (
            self.prefetch_related("road", "organization")
            .all()
            .order_by("road")
        )

    def get_by_year_and_organization(self, year, organization):
        return self.filter(year__year=year, organization=organization)

    def get_years(self):
        return self.values_list("year__year")

    def get_years_by_organization_landscape(self, user):
        return self.values_list("year__year").filter(
            road_address__len=1, organization=user.organization
        )

    def get_by_year_month_organization_sum(self, year, month, organization):
        base_queryset = (
            self.values("organization")
            .annotate(
                money_amount_plan_sum=Subquery(
                    YearlyProductionPlan.objects.values("organization")
                    .filter(organization=organization)
                    .annotate(
                        a=Sum(
                            Coalesce(
                                Case(
                                    When(
                                        Q(year__year=year),
                                        then="money_amount_plan",
                                    ),
                                    default=0,
                                ),
                                0,
                            )
                        )
                    )
                    .values("a"),
                ),
                production_money_until_month=Sum(
                    Coalesce(
                        Case(
                            When(
                                Q(
                                    monthly_prod__month__month__lte=month,
                                    year__year=year,
                                ),
                                then="monthly_prod__base_prod__money_amount",
                            ),
                            default=0,
                        ),
                        0,
                    )
                ),
                monthly_plan_sum_until_month=Sum(
                    Coalesce(
                        Case(
                            When(
                                Q(
                                    monthly_prod__month__month__lte=month,
                                    year__year=year,
                                ),
                                then="monthly_prod__monthly_plan_money",
                            ),
                            default=0,
                        ),
                        0,
                    )
                ),
                monthly_plan_sum_month=Sum(
                    Coalesce(
                        Case(
                            When(
                                Q(
                                    monthly_prod__month__month=month,
                                    year__year=year,
                                ),
                                then="monthly_prod__monthly_plan_money",
                            ),
                            default=0,
                        ),
                        0,
                    )
                ),
                monthly_financing_sum_until_month=Sum(
                    Coalesce(
                        Case(
                            When(
                                Q(
                                    monthly_prod__month__month__lte=month,
                                    year__year=year,
                                ),
                                then="monthly_prod__financing",
                            ),
                            default=0,
                        ),
                        0,
                    )
                ),
                monthly_financing_sum_month=Sum(
                    Coalesce(
                        Case(
                            When(
                                Q(
                                    monthly_prod__month__month=month,
                                    year__year=year,
                                ),
                                then="monthly_prod__financing",
                            ),
                            default=0,
                        ),
                        0,
                    )
                ),
                production_money_month=Sum(
                    Coalesce(
                        Case(
                            When(
                                Q(
                                    monthly_prod__month__month=month,
                                    year__year=year,
                                ),
                                then="monthly_prod__base_prod__money_amount",
                            ),
                            default=0,
                        ),
                        0,
                    )
                ),
            )
            .filter(year__year=year, organization=organization)
        )

        return base_queryset

    def get_by_year_month_organization(self, year, month, organization):
        return (
            self.annotate(
                production_money_until_month=Sum(
                    Coalesce(
                        Case(
                            When(
                                Q(
                                    monthly_prod__month__month__lte=month,
                                    year__year=year,
                                ),
                                then="monthly_prod__base_prod__money_amount",
                            ),
                            default=0,
                        ),
                        0,
                    )
                ),
                monthly_plan_sum_until_month=Sum(
                    Coalesce(
                        Case(
                            When(
                                Q(
                                    monthly_prod__month__month__lte=month,
                                    year__year=year,
                                ),
                                then="monthly_prod__monthly_plan_money",
                            ),
                            default=0,
                        ),
                        0,
                    )
                ),
                monthly_plan_sum_month=Sum(
                    Coalesce(
                        Case(
                            When(
                                Q(
                                    monthly_prod__month__month=month,
                                    year__year=year,
                                ),
                                then="monthly_prod__monthly_plan_money",
                            ),
                            default=0,
                        ),
                        0,
                    )
                ),
                monthly_financing_sum_until_month=Sum(
                    Coalesce(
                        Case(
                            When(
                                Q(
                                    monthly_prod__month__month__lte=month,
                                    year__year=year,
                                ),
                                then="monthly_prod__financing",
                            ),
                            default=0,
                        ),
                        0,
                    )
                ),
                monthly_financing_sum_month=Sum(
                    Coalesce(
                        Case(
                            When(
                                Q(
                                    monthly_prod__month__month=month,
                                    year__year=year,
                                ),
                                then="monthly_prod__financing",
                            ),
                            default=0,
                        ),
                        0,
                    )
                ),
                production_money_month=Sum(
                    Coalesce(
                        Case(
                            When(
                                Q(
                                    monthly_prod__month__month=month,
                                    year__year=year,
                                ),
                                then="monthly_prod__base_prod__money_amount",
                            ),
                            default=0,
                        ),
                        0,
                    )
                ),
            )
            .values(
                "production_money_until_month",
                "production_money_month",
                "monthly_plan_sum_until_month",
                "monthly_plan_sum_month",
                "monthly_financing_sum_until_month",
                "monthly_financing_sum_month",
                "road__title",
                "road_address",
                "road__road_type",
                "money_amount_plan",
            )
            .filter(year__year=year, organization=organization)
            .order_by("road__road_type")
        )


class YearlyProductionPlanManager(models.Manager):
    def get_queryset(self):
        return YearlyProductionPlanQuerySet(model=self.model, using=self._db)

    def get_years_by_organization(self, user):
        return self.get_queryset().get_years_by_organization(user)

    def get_years_by_organization_landscape(self, user):
        return self.get_queryset().get_years_by_organization_landscape(user)

    def get_by_year_and_organization(self, year, organization):
        return self.get_queryset().get_by_year_and_organization(
            year=year, organization=organization
        )

    def get_years(self):
        return self.get_queryset().get_years()

    def get_by_year_month_organization(self, year, month, organization):
        return self.get_queryset().get_by_year_month_organization(
            year=year, month=month, organization=organization
        )

    def get_all(self):
        return self.get_queryset().get_all()

    def get_by_year_month_organization_sum(self, year, month, organization):
        return self.get_queryset().get_by_year_month_organization_sum(
            year=year, month=month, organization=organization
        )


class YearlyProductionPlan(BaseModel):
    road = models.ForeignKey(
        Road, on_delete=models.CASCADE, related_name="yearly"
    )
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    money_amount_plan = models.DecimalField(max_digits=13, decimal_places=2)
    road_address = ArrayField(models.FloatField(), max_length=2)
    year = models.DateField()
    objects = YearlyProductionPlanManager()

    class Meta:
        unique_together = ("organization", "road", "road_address", "year")

    def __str__(self):
        return self.road.title


class MonthlyProductionPlanQuerySet(models.QuerySet):
    def get_by_organization(self, user):
        return self.annotate(
            yearly_prod_plan=YearlyProductionPlan(
                organization=user.organization
            )
        )

    def get_by_year_and_organization(self, user, year, month):
        return self.filter(
            yearly_prod_plan__organization=user.organization,
            yearly_prod_plan__year__year=year,
            month__month=month,
        ).values(
            "id",
            "yearly_prod_plan__road_address",
            road=F("yearly_prod_plan__road__title"),
        )


class MonthlyProductionPlanManger(models.Manager):
    def get_queryset(self):
        return MonthlyProductionPlanQuerySet(model=self.model, using=self._db)

    def get_by_organization(self, user):
        return self.get_queryset().get_by_organization(user)

    def get_by_year_and_organization(self, user, year, month):
        return self.get_queryset().get_by_year_and_organization(
            user, year, month
        )

    def get_list(self):
        return (
            self.get_queryset()
            .select_related(
                "yearly_prod_plan",
                "yearly_prod_plan__road",
                "yearly_prod_plan__organization",
            )
            .all()
        )


class MonthlyProductionPlan(BaseModel):
    yearly_prod_plan = models.ForeignKey(
        YearlyProductionPlan,
        on_delete=models.CASCADE,
        related_name="monthly_prod",
    )
    monthly_plan_money = models.DecimalField(max_digits=13, decimal_places=2)
    financing = models.DecimalField(max_digits=13, decimal_places=2)
    month = models.DateField()
    objects = MonthlyProductionPlanManger()

    def __str__(self):
        return (
            f"{self.yearly_prod_plan.road.title} "
            f"{self.yearly_prod_plan.year.year} "
            f"{self.month.month}"
        )

    class Meta:
        ordering = ("-id",)
        unique_together = ("yearly_prod_plan", "month")


class BaseModelProductionQuerySet(models.QuerySet):
    pass


class BaseModelProductionManager(models.Manager):
    def get_queryset(self):
        return BaseModelProductionQuerySet(model=self.model, using=self._db)


class BaseModelProduction(BaseModel):
    class ProductionType(models.TextChoices):
        IRRIGATION = "IRRIGATION"
        PLANTING = "PLANTING"
        SAVING = "SAVING"
        LANDSCAPE = "LANDSCAPE"

    monthly_prod_plan = models.ForeignKey(
        MonthlyProductionPlan,
        on_delete=models.CASCADE,
        related_name="base_prod",
    )
    quantity = models.IntegerField()
    money_amount = models.DecimalField(max_digits=13, decimal_places=2)
    LSH = models.DecimalField(max_digits=13, decimal_places=2)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    road_address = ArrayField(models.FloatField(), max_length=2)
    production_type = models.CharField(
        choices=ProductionType.choices, max_length=20
    )
    objects = BaseModelProductionManager()

    class Meta:
        ordering = ("-id",)


class SavingProductionQueryset(models.QuerySet):
    def get_by_organization(self, user):
        return self.filter(
            organization=user.organization,
            production_type=BaseModelProduction.ProductionType.SAVING,
        )


class SavingProductionManager(models.Manager):
    def get_queryset(self):
        return SavingProductionQueryset(model=self.model, using=self._db)

    def get_by_organization(self, user):
        return self.get_queryset().get_by_organization(user)


class SavingJobProduction(BaseModelProduction):
    objects = SavingProductionManager()

    class Meta:
        proxy = True


class IrrigationProductionQueryset(models.QuerySet):
    def get_by_organization(self, user):
        return self.filter(
            organization=user.organization,
            production_type=BaseModelProduction.ProductionType.IRRIGATION,
        )


class IrrigationProductionManager(models.Manager):
    def get_queryset(self):
        return IrrigationProductionQueryset(model=self.model, using=self._db)

    def get_by_organization(self, user):
        return self.get_queryset().get_by_organization(user)


class IrrigationProduction(BaseModelProduction):
    objects = IrrigationProductionManager()

    class Meta:
        proxy = True


class PlantingProductionQueryset(models.QuerySet):
    def get_by_organization(self, user):
        return self.filter(
            organization=user.organization,
            production_type=BaseModelProduction.ProductionType.PLANTING,
        )


class PlantingProductionManager(models.Manager):
    def get_queryset(self):
        return PlantingProductionQueryset(model=self.model, using=self._db)

    def get_by_organization(self, user):
        return self.get_queryset().get_by_organization(user)


class PlantingProduction(BaseModelProduction):
    objects = PlantingProductionManager()

    class Meta:
        proxy = True


class LandscapeJobProductionQueryset(models.QuerySet):
    def get_by_organization(self, user):
        return self.filter(
            organization=user.organization,
            production_type=BaseModelProduction.ProductionType.LANDSCAPE,
        )


class LandscapeJobProductionManager(models.Manager):
    def get_queryset(self):
        return LandscapeJobProductionQueryset(model=self.model, using=self._db)

    def get_by_organization(self, user):
        return self.get_queryset().get_by_organization(user)


class LandscapeJobProduction(BaseModelProduction):
    objects = LandscapeJobProductionManager()

    class Meta:
        proxy = True
