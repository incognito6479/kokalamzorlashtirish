import math
import os
from datetime import date

from django import template

from pitomnik.models import IrrigationType, Plant, PlantedPlants
from regionroad.models import Road

register = template.Library()


@register.filter
def irrigation_type_label(obj):
    return IrrigationType(obj).label


@register.filter
def array_to_range_str(obj):
    for i in range(len(obj)):
        if round(obj[i]) - obj[i] == 0:
            obj[i] = int(obj[i])
    return "-".join(repr(e) for e in obj)


@register.filter
def plant_source_label(obj):
    return PlantedPlants.SourceType(obj).label


@register.filter(name="sub", is_safe=True)
def sub(number=None, number_op=None):
    return number - number_op


@register.filter
def plant_type_label(obj):
    return Plant.PlantType(obj).label


@register.filter
def road_type_label(obj):
    return Road.RoadType(obj).label


@register.filter
def filename(value):
    from django.db.models.fields.files import ImageFieldFile

    if isinstance(value.initial, ImageFieldFile):
        return os.path.basename(value.initial.name)
    return " Расм танланг..."


@register.filter
def planting_side_label(obj):
    return PlantedPlants.PlantingSide(obj).label


@register.filter
def get_status_pitomnik_plant(obj):
    if obj:
        if obj <= date.today():
            return "Тайёр"
    return "Тайёр эмас"


@register.filter
def get_decimal(obj):
    if round(obj) - obj == 0:
        return int(obj)
    return obj


@register.filter
def round_upper(obj):
    if isinstance(obj, float):
        return math.ceil(obj)
    return obj


road_length = {"Халқаро": 3993, "Давлат": 14203, "Маҳаллий": 24673}


@register.filter(name="road_slice")
def get_road_length(road_type):
    return road_length[road_type]


@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]
    return d.urlencode()

