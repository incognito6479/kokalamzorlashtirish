from django.urls import include, path

from .views import (
    CreateVehicleTypeView,
    CreateVehicleView,
    DeleteVehicleView,
    DownloadVehicleView,
    ListVehicleAdminView,
    ListVehicleByOrganizationView,
    ListVehicleTypesCountByOrganization,
    ListVehicleTypeView,
    ListVehicleView,
    UpdateVehicleTypeView,
    UpdateVehicleView,
)

app_name = "vehicles"
admin = [
    path("", ListVehicleAdminView.as_view(), name="organization"),
    path(
        "region/<int:pk>/list-by-organization/",
        ListVehicleByOrganizationView.as_view(),
        name="list_by_organization",
    ),
    path(
        "list-by-type",
        ListVehicleTypesCountByOrganization.as_view(),
        name="list_by_type",
    ),
    path("type", ListVehicleTypeView.as_view(), name="list_type"),
    path("add-type", CreateVehicleTypeView.as_view(), name="add_type"),
    path(
        "<int:pk>/update-type",
        UpdateVehicleTypeView.as_view(),
        name="change_type",
    ),
    path("download/<int:pk>/", DownloadVehicleView.as_view(), name="download"),
]
local = [
    path("", ListVehicleView.as_view(), name="list"),
    path("add", CreateVehicleView.as_view(), name="add"),
    path("<int:pk>/update/", UpdateVehicleView.as_view(), name="change"),
    path("<int:pk>/delete/", DeleteVehicleView.as_view(), name="delete"),
]
urlpatterns = [
    path("admins/", include((admin, "admin"))),
    path("locals/", include((local, "local"))),
]
