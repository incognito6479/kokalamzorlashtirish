from django.db import models

from django_filters import CharFilter, FilterSet

from .models import (
    IrrigationProduction,
    LandscapeJobProduction,
    MonthlyProductionPlan,
    PlantingProduction,
    SavingJobProduction,
    YearlyProductionPlan,
)


class BaseFilter(FilterSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, value in self.filters.items():
            self.filters[key].label = ""


class BaseFilterMeta:
    filter_overrides = {
        models.CharField: {
            "filter_class": CharFilter,
            "extra": lambda f: {
                "lookup_expr": "icontains",
            },
        },
    }


class IrrigationProductionFilter(BaseFilter):
    class Meta(BaseFilterMeta):
        model = IrrigationProduction
        fields = [
            "monthly_prod_plan__yearly_prod_plan__road",
            "monthly_prod_plan__yearly_prod_plan__road__code",
        ]


class SavingProductionFilter(BaseFilter):
    class Meta(BaseFilterMeta):
        model = SavingJobProduction
        fields = [
            "monthly_prod_plan__yearly_prod_plan__road",
            "monthly_prod_plan__yearly_prod_plan__road__code",
        ]


class PlantingProductionFilter(BaseFilter):
    class Meta(BaseFilterMeta):
        model = PlantingProduction
        fields = [
            "monthly_prod_plan__yearly_prod_plan__road",
            "monthly_prod_plan__yearly_prod_plan__road__code",
        ]


class LandscapeProductionFilter(BaseFilter):
    class Meta(BaseFilterMeta):
        model = LandscapeJobProduction
        fields = [
            "monthly_prod_plan__yearly_prod_plan__road",
            "monthly_prod_plan__yearly_prod_plan__road__code",
        ]


class YearlyProductionFilter(BaseFilter):
    class Meta(BaseFilterMeta):
        models = YearlyProductionPlan
        fields = ["organization__name", "year", "road__title"]


class MonthlyProductionFilter(BaseFilter):
    class Meta(BaseFilterMeta):
        models = MonthlyProductionPlan
        fields = ["yearly_prod_plan__road__title", "year", "road__title"]
