from django.db import models
from django.forms import TextInput

import django_filters
from django_filters import CharFilter

from vehicles.models import Vehicle


class VehicleFilter(django_filters.FilterSet):
    manufactured_date = CharFilter(widget=TextInput(attrs={"hidden": True}))

    class Meta:
        model = Vehicle
        fields = [
            "name",
            "manufactured_date",
            "registration_plate",
            "GPS_status",
            "storage_site",
            "tech_state",
        ]
        filter_overrides = {
            models.CharField: {
                "filter_class": django_filters.CharFilter,
                "extra": lambda f: {
                    "lookup_expr": "icontains",
                },
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, value in self.filters.items():
            self.filters[key].label = ""
