from django import forms
from django.utils.translation import gettext_lazy as _

from regionroad.models import RoadDistrict


class RoadDistrictForm(forms.ModelForm):
    class Meta:
        model = RoadDistrict
        fields = [
            "requirement",
        ]
        labels = {
            "requirement": _("Кўкаламзорлаштиришга талаб"),
        }
