from django.contrib import admin
from .models import (
    PlantingProduction,
    SavingJobProduction,
    IrrigationProduction,
    LandscapeJobProduction,
    MonthlyProductionPlan,
    YearlyProductionPlan,
    BaseModelProduction,

)


@admin.register(BaseModelProduction)
class BaseModelProductionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "production_type",
        "road_address",
        "money_amount",
        "quantity",
        "LSH",
        "get_month",

    )

    def get_month(self, obj):
        return f"{obj.monthly_prod_plan.month.strftime('%B')} {obj.monthly_prod_plan.yearly_prod_plan.year.year}"


@admin.register(PlantingProduction)
class PlantingProductionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "road_title",
        "road_address",
        "money_amount",
        "quantity",
        "LSH",
        "get_month"
    )

    def road_title(self, obj):
        return obj.monthly_prod_plan.yearly_prod_plan.road.title

    def get_month(self, obj):
        return f"{obj.monthly_prod_plan.month.strftime('%B')} {obj.monthly_prod_plan.yearly_prod_plan.year.year}"


@admin.register(SavingJobProduction)
class SavingJobProductionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "get_road_title",
        "road_address",
        "money_amount",
        "quantity",
        "LSH",
        "get_month_year"
    )

    def get_month_year(self, obj):
        return f"{obj.monthly_prod_plan.month.strftime('%B')} {obj.monthly_prod_plan.yearly_prod_plan.year.year}"

    def get_road_title(self, obj):
        return obj.monthly_prod_plan.yearly_prod_plan.road.title


@admin.register(IrrigationProduction)
class IrrigationProductionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "get_road_title",
        "road_address",
        "money_amount",
        "quantity",
        "LSH",
        "get_month_year"
    )

    def get_month_year(self, obj):
        return f"{obj.monthly_prod_plan.month.strftime('%B')} {obj.monthly_prod_plan.yearly_prod_plan.year.year}"

    def get_road_title(self, obj):
        return obj.monthly_prod_plan.yearly_prod_plan.road.title


@admin.register(LandscapeJobProduction)
class LandscapeJobProductionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "get_road_title",
        "road_address",
        "money_amount",
        "quantity",
        "LSH",
        "get_month_year"
    )

    def get_month_year(self, obj):
        return f"{obj.monthly_prod_plan.month.strftime('%B')} {obj.monthly_prod_plan.yearly_prod_plan.year.year}"

    def get_road_title(self, obj):
        return obj.monthly_prod_plan.yearly_prod_plan.road.title


@admin.register(YearlyProductionPlan)
class YearPlanningAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "road",
        "road_address",
        "money_amount_plan",
        "organization",
        "get_year",
    )

    def get_year(self, obj):
        return obj.year.year


@admin.register(MonthlyProductionPlan)
class MonthlyPlanningAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "yearly_prod_plan",
        "monthly_plan_money",
        "financing",
        "get_month_year"
    )

    def get_month_year(self, obj):
        return f"{obj.month.strftime('%B')} {obj.yearly_prod_plan.year.year}"
