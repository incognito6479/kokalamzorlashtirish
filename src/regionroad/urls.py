from django.urls import include, path

from regionroad.views import (
    GetDistrictPlantQuantity,
    GetRegionDistrict,
    GetRegionPlantQuantity,
    GetRegions,
    GetRepublicPlantQuantity,
    RoadDistrictCreateView,
    RoadDistrictDeleteView,
    RoadDistrictListView,
    RoadDistrictUpdateView,
    GetUzbJson
)

from .views import GetJson

app_name = "regionroad"
api_urls = [
    path("coordinates/", GetJson.as_view(), name="api_coordinates"),
    path("regions/", GetRegions.as_view(), name="api_regions"),
    path(
        "<int:pk>/districts/",
        GetRegionDistrict.as_view(),
        name="api_districts",
    ),
    path(
        "<int:pk>/districtplants/",
        GetDistrictPlantQuantity.as_view(),
        name="api_districtplants",
    ),
    path(
        "<int:pk>/regionplants/",
        GetRegionPlantQuantity.as_view(),
        name="api_regionplants",
    ),
    path("cordinates/", GetUzbJson.as_view(), name="uzb_json"),
    path("republicplants/", GetRepublicPlantQuantity.as_view(), name="api_republicplants")
]

urlpatterns = [
    path("list/", RoadDistrictListView.as_view(), name="road-district-list"),
    path(
        "create/",
        RoadDistrictCreateView.as_view(),
        name="road-district-create",
    ),
    path(
        "<int:pk>/update/",
        RoadDistrictUpdateView.as_view(),
        name="road-district-update",
    ),
    path(
        "<int:pk>/delete/",
        RoadDistrictDeleteView.as_view(),
        name="road-district-delete",
    ),
    path("api/", include((api_urls, "api"))),
]
