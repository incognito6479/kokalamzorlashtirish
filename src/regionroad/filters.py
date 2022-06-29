from django.db import models

import django_filters

from regionroad.models import RoadDistrict


class BaseFilter(django_filters.FilterSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key, value in self.filters.items():
            self.filters[key].label = ""


class BaseFilterMeta:
    filter_overrides = {
        models.CharField: {
            "filter_class": django_filters.CharFilter,
            "extra": lambda f: {
                "lookup_expr": "icontains",
            },
        },
    }


class RoadFilter(BaseFilter):
    class Meta(BaseFilterMeta):
        model = RoadDistrict
        fields = ["road", "road__code"]
