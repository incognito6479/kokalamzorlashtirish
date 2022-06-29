from decimal import DivisionUndefined

from django import template

from account.models import Organization
from regionroad.models import Road

register = template.Library()

MONTH_KEY_VAL = {
    1: "Январь",
    2: "Февраль",
    3: "Март",
    4: "Апрель",
    5: "Май",
    6: "Июнь",
    7: "Июль",
    8: "Август",
    9: "Сентабрь",
    10: "Октябрь",
    11: "Ноябрь",
    12: "Декабрь",
}


@register.filter(name="to_string")
def month_to_string(number):
    try:
        number = int(number)
        return MONTH_KEY_VAL[number]
    except TypeError:
        return ""


@register.filter
def array_to_range_str(obj):
    return "-".join(repr(e) for e in obj)


@register.filter(name="road_type")
def road_type_label(obj):
    return Road.RoadType(obj).label


@register.filter(name="to_org_string")
def org_to_string(org):
    try:
        id = int(org)
        org = Organization.objects.get(id=id)
        return org.name
    except TypeError or org.DoesNotExist:
        return ""


@register.filter(name="procent")
def percent(number=None, number_op=None):
    try:
        return round(((int(number) / int(number_op)) * 100), 2)
    except DivisionUndefined and TypeError and ZeroDivisionError:
        return "-"
