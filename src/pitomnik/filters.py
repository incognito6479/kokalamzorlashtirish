from datetime import date
from django.db import models
from django.forms.widgets import DateInput, TextInput
from django_filters import (
    CharFilter,
    ChoiceFilter,
    DateFilter,
    DateRangeFilter,
    FilterSet,
    ModelChoiceFilter
)
from .models import (
    Irrigation,
    NewIrrigation,
    Pitomnik,
    PitomnikPlants,
    Plant,
    PlantedPlants,
    SavingJob,
)
from account.models import Organization


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


class DateRangeFilter(BaseFilter):
    start_date = DateFilter(
        field_name="created_at",
        lookup_expr=("gt"),
        label="",
        widget=DateInput(attrs={"id": "datepicker", "type": "date"}),
    )
    end_date = DateFilter(
        field_name="created_at",
        lookup_expr=("lt"),
        label="",
        widget=DateInput(attrs={"id": "datepicker", "type": "date"}),
    )
    date_range = DateRangeFilter(field_name="created_at", label="")


class IrrigationFilter(DateRangeFilter):
    class Meta:
        model = Irrigation
        fields = ["road_district__road", "irrigation_type"]


class SavingJobFilter(BaseFilter):
    class Meta:
        model = SavingJob
        fields = ["road_district__road"]


class PlantFilter(BaseFilter):
    class Meta(BaseFilterMeta):
        model = Plant
        fields = ["name", "type"]


class NewIrrigationFilter(DateRangeFilter):
    class Meta:
        model = NewIrrigation
        fields = ["road_district__road"]


def get_roaddistrict_by_org(request):
    queryset = PlantedPlants.objects.filter(pitomnik_id__organization_id=request.user.organization_id)
    for i in queryset:
        print(i)
    return queryset


class PlantedPlantFilter(BaseFilter):
    # road_district__district = ModelChoiceFilter(queryset=get_roaddistrict_by_org)

    class Meta(BaseFilterMeta):
        model = PlantedPlants
        fields = [
            "road_district__district",
            "road_district__road",
            "road_district__road__code",
            "plant",
        ]


def pitomnik_list(request):
    id = request.GET.get('pitomnik__organization', '')
    queryset = Pitomnik.objects.all()
    if id.isdigit():
        queryset = queryset.filter(organization_id=int(id))
    else:
        return queryset.filter(id=0)

    return queryset


def organization_list(request):
    pitomnik__organization = Organization.objects.exclude(name__in=['Admin', 'УП Ўзйулкукаламзорлаштириш'])
    queryset = pitomnik__organization
    return queryset


class PitomnikPlantFilter(BaseFilter):
    STATUS_CHOICES = (
        ("ready", "Тайёр ўсимликлар"),
        ("not_ready", "Тайёр эмас ўсимликлар"),
    )
    status = ChoiceFilter(choices=STATUS_CHOICES, method="get_status")
    planted_date = CharFilter(widget=TextInput(attrs={"hidden": True}))
    readiness_date = CharFilter(widget=TextInput(attrs={"hidden": True}))

    pitomnik = ModelChoiceFilter(queryset=pitomnik_list)

    pitomnik__organization = ModelChoiceFilter(queryset=organization_list)

    class Meta(BaseFilterMeta):
        model = PitomnikPlants

        fields = [
            # "pitomnik",
            "plant",
            "plant__type",
            "planted_date",
            "readiness_date",
            "status",
            # "pitomnik__organization",
        ]

    def get_status(self, queryset, name, value):
        if value == "ready":
            return queryset.filter(readiness_date__lte=date.today())
        elif value == "not_ready":
            return queryset.filter(readiness_date__gt=date.today())
        return queryset


class PitomnikFilter(BaseFilter):
    def __init__(self, attribute=None, **kwargs):
        organization = kwargs.pop("organization")
        super().__init__(**kwargs)

    STATUS_CHOICES = (
        ("ready", "Тайёр ўсимликлар"),
        ("not_ready", "Тайёр эмас ўсимликлар"),
    )
    status = ChoiceFilter(choices=STATUS_CHOICES, method="get_status")
    planted_date = CharFilter(widget=TextInput(attrs={"hidden": True}))
    readiness_date = CharFilter(widget=TextInput(attrs={"hidden": True}))

    class Meta(BaseFilterMeta):
        model = PitomnikPlants

        fields = [
            "pitomnik",
            "plant",
            "plant__type",
            "planted_date",
            "readiness_date",
            "status",
        ]

    def get_status(self, queryset, name, value):
        if value == "ready":
            return queryset.filter(readiness_date__lte=date.today())
        elif value == "not_ready":
            return queryset.filter(readiness_date__gt=date.today())
        return queryset
