from django import forms
from django.contrib import admin

from pitomnik.models import (
    Irrigation,
    LandScapeJob,
    Pitomnik,
    PitomnikImage,
    PitomnikPlantImage,
    PitomnikPlants,
    PitomnikSavingJob,
    PitomnikSavingJobImage,
    Plant,
    PlantedPlantImage,
    PlantedPlants,
    SavingJob,
)
from regionroad.models import RoadDistrict


@admin.register(Plant)
class PlantAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "type", "added_by", "created_at")
    list_filter = ("type",)
    search_fields = ("name", "id")


class PitomnikPlantsImageAdmin(admin.TabularInline):
    model = PitomnikPlantImage
    extra = 1
    fields = ["id", "image"]
    readonly_fields = ["id"]


class PitomnikPlantAdmin(admin.ModelAdmin):
    model = PitomnikPlants
    inlines = [PitomnikPlantsImageAdmin]
    list_display = (
        "id",
        "get_pitomnik",
        "plant",
        "action_type",
        "quantity",
        "created_at",
        "readiness_date",
        "get_plant_type",
        "plant_type",
        "get_organization",
    )
    list_filter = (
        "pitomnik",
        "plant__type",
        "action_type",
        "pitomnik__organization",
    )

    def get_plant(self, obj):
        return obj.plant.name

    def get_plant_type(self, obj):
        return Plant.PlantType(obj.plant.type).label

    def get_pitomnik(self, obj):
        return obj.pitomnik.name

    def get_organization(self, obj):
        return obj.pitomnik.organization.name


admin.site.register(PitomnikPlants, PitomnikPlantAdmin)


class PlantedPlantsImageAdmin(admin.TabularInline):
    model = PlantedPlantImage
    extra = 1
    fields = ["id", "image"]
    readonly_fields = ["id"]


@admin.register(PlantedPlants)
class PlantedPlantsAdmin(admin.ModelAdmin):
    inlines = [PlantedPlantsImageAdmin]
    list_display = (
        "id",
        "plant_source",
        "get_plant",
        "get_plant_type",
        "get_pitomnik",
        "quantity",
        "road_from",
        "road_to",
        "planting_side",
        "added_by",
        "get_road",
        "created_at",
    )
    list_filter = (
        "plant_source",
        "pitomnik",
        "plant__type",
        "road_district__district__region",
        "planting_side",
    )

    def get_plant(self, obj):
        return obj.plant.name

    def get_plant_type(self, obj):
        return Plant.PlantType(obj.plant.type).label

    def get_pitomnik(self, obj):
        return obj.pitomnik

    def get_road(self, obj):
        return obj.road_district.road.title


class PitomnikImageAdmin(admin.TabularInline):
    model = PitomnikImage
    extra = 1
    fields = ["id", "image"]
    readonly_fields = ["id"]


class PitomnikAdmin(admin.ModelAdmin):
    inlines = [PitomnikImageAdmin]
    list_display = (
        "id",
        "name",
        "area",
        "address",
        "added_by",
        "organization",
        "kontr",
        "get_organization",
    )
    list_filter = ("organization",)

    def get_organization(self, obj):
        return obj.organization.name

    get_organization.short_description = "Organization"


admin.site.register(Pitomnik, PitomnikAdmin)


class SavingJobFormSetAdmin(forms.BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.road_district_choices = [
            *forms.ModelChoiceField(
                RoadDistrict.objects.select_related("road")
            ).choices
        ]

    def get_form_kwargs(self, index):
        kwargs = super().get_form_kwargs(index)
        kwargs["road_district_choices"] = self.road_district_choices
        return kwargs


class SavingJobAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        road_district_choices = kwargs.pop("road_district_choices", None)
        super().__init__(*args, **kwargs)
        if road_district_choices:
            self.fields["road_district"].choices = road_district_choices


@admin.register(SavingJob)
class SavingJobAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "road_district",
        "road_from",
        "road_to",
        "dig_quantity",
        "dig_len",
        "organic_len",
        "organic_quantity",
        "workers_quantity",
        "technique_quantity",
        "created_at",
    )

    list_editable = ("road_district", "road_from", "road_to")

    def get_road_title(self, obj):
        return obj.road_district.road.title

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields[
            "road_district"
        ].queryset = RoadDistrict.objects.select_related("road").order_by(
            "-id"
        )
        return form

    def get_changelist_form(self, request, **kwargs):
        kwargs["form"] = SavingJobAdminForm
        return super().get_changelist_form(request, **kwargs)

    def get_changelist_formset(self, request, **kwargs):
        kwargs["formset"] = SavingJobFormSetAdmin
        return super().get_changelist_formset(request, **kwargs)


@admin.register(Irrigation)
class IrrigationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "road_district",
        "road_slice",
        "tree_quantity",
        "length",
        "irrigation_type",
    )


@admin.register(LandScapeJob)
class LandScapeJob(admin.ModelAdmin):
    list_display = (
        "id",
        "road_district",
        "road_slice",
        "round_quantity",
        "round_area",
        "cross_quantity",
        "cross_area",
        "panno_quantity",
        "road_side_length",
    )


admin.site.register(PitomnikSavingJob)
admin.site.register(PitomnikSavingJobImage)
