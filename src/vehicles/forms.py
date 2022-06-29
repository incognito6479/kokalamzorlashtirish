from django.forms import ModelForm
from django.forms.fields import CharField
from django.utils.translation import gettext_lazy as _

from .models import Vehicle, VehicleTypes, validate_registration_plate


class LicencePlate(CharField):
    default_validators = [
        validate_registration_plate,
    ]


class VehicleAddForm(ModelForm):
    class Meta:
        model = Vehicle
        fields = (
            "type",
            "name",
            "manufactured_date",
            "registration_plate",
            "inventory",
            "GPS_status",
            "balance_value",
            "aging_value",
            "mileage_value_start_year",
            "mileage_value_report_time",
            "tech_state",
            "storage_site",
        )
        labels = {
            "type": _("Техника тури"),
            "name": _("Техникалар номи"),
            "manufactured_date": _("И/Ч Йили (сана)"),
            "registration_plate": _("Давалат рақами"),
            "GPS_status": _("GPS системаси урнатилганлиги"),
            "balance_value": _("Баланс киймати (млн.сум)"),
            "aging_value": _("Юрган масофаси(пробег),Маш/соати"),
            "mileage_value_start_year": _("Йил бошида (км/маш.час)"),
            "mileage_value_report_time": _("Ҳисобот даврида (км/маш.час)"),
            "inspection": _("Текширув"),
            "tech_state": _("Техник ҳолати"),
            "inventory": _("Инвентар рақами"),
            "storage_site": _("саклаш холати(айвонда/очик хавода)"),
        }


class VehicleUpdateForm(ModelForm):
    class Meta:
        model = Vehicle
        fields = (
            "type",
            "name",
            "manufactured_date",
            "registration_plate",
            "inventory",
            "GPS_status",
            "balance_value",
            "aging_value",
            "mileage_value_start_year",
            "mileage_value_report_time",
            "tech_state",
            "storage_site",
        )
        labels = {
            "type": _("Техника тури"),
            "name": _("Техникалар номи"),
            "manufactured_date": _("И/Ч Йили (сана)"),
            "registration_plate": _("Давалат рақами"),
            "GPS_status": _("GPS системаси урнатилганлиги"),
            "balance_value": _("Баланс киймати (млн.сум)"),
            "aging_value": _("Юрган масофаси(пробег),Маш/соати"),
            "mileage_value_start_year": _("Йил бошида (км/маш.час)"),
            "mileage_value_report_time": _("Ҳисобот даврида (км/маш.час)"),
            "inspection": _("Текширув"),
            "inventory": _("Инвентар рақами"),
            "tech_state": _("Техник ҳолати"),
            "storage_site": _("саклаш холати(айвонда/очик хавода)"),
        }


class VehicleTypesForm(ModelForm):
    class Meta:
        model = VehicleTypes
        fields = ("name",)
        labels = {
            "name": _("Техника тури номи"),
        }
