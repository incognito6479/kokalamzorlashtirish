from django.contrib import admin

from regionroad.models import District, Region, Road, RoadDistrict


class RoadAdmin(admin.ModelAdmin):
    def region(self, obj):
        return obj.title

    list_display = [
        "id",
        "title",
        "code",
        "road_type",
    ]
    list_filter = ["road_type", "roaddistrict__district__region"]


class RegionAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "code"]


class DistrictAdmin(admin.ModelAdmin):
    search_fields = ["name"]
    list_display = ["id", "name", "get_region"]
    list_filter = ("region",)

    def get_region(self, obj):
        return obj.region.name


class RoadDistrictAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "road",
        "district",
        "road_from",
        "road_to",
        "requirement",
        "get_road_type",
    ]

    list_filter = ("road__road_type", "district__region")

    def get_road_type(self, obj):
        return Road.RoadType(obj.road.road_type).label


admin.site.register(RoadDistrict, RoadDistrictAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Road, RoadAdmin)
admin.site.register(District, DistrictAdmin)
