from django.conf.urls import include
from django.urls import path

from .views.irrigation import (
    CreateIrrigationView,
    DeleteIrrigationView,
    AdminDeleteIrrigationView,
    IrrigationAdminByOrganization,
    IrrigationFilteredListView,
    IrrigationFilteredListViewAdmin,
    ListIrrigationImages,
    UpdateIrrigationView,
    AdminUpdateIrrigationView,
)
from .views.pitomnik import (
    AdminListPitomnikView,
    CreatePitomnikView,
    DeletePitomnikView,
    ListPitomnikImages,
    UpdatePitomnikView,
)
from .views.plant import (
    CreatePlantView,
    DeletePlantView,
    ListPlantView,
    UpdatePlantView,
)
from .views.planted_plant import (
    AdminListPlantedPlantView,
    CreatePlantedPlant,
    DeletePlantedPlant,
    DownloadPlantedPlant,
    ListPlantedPlantByRegionAdminView,
    ListPlantedPlantByRoadAdminView,
    ListPlantedPlantByRoadView,
    ListPlantedPlantImage,
    ListPlantedPlantView,
    LoadDistrictView,
    LoadPlantView,
    LoadRoadView,
    UpdateListPlantedPlantView,
)

from .views.landscape_job import (
    CreateLandScapeJob,
    DeleteLandScapeJob,
    AdminDeleteLandScapeJob,
    ListLandScapeJob,
    ListLandScapeJobAdmin,
    ListLandScapeJobByOrganizationAdmin,
    ListLandScapeJobImages,
    UpdateLandScapeJob,
    AdminUpdateLandScapeJob,
)
from .views.map import index, road_add, road_add_form, road_change, road_delete
from .views.new_irrigation import (
    CreateNewIrrigationView,
    DeleteNewIrrigationView,
    AdminDeleteNewIrrigationView,
    ListNewIrrigationAdminView,
    ListNewIrrigationByOrganizationAdmin,
    ListNewIrrigationImages,
    ListNewIrrigationView,
    UpdateNewIrrigationView,
    AdminUpdateNewIrrigationView,
)
from .views.pitomnik import ListPitomnikView
from .views.pitomnik_plant import (
    AdminPitomnikPlantListView,
    AdminPitomnikPlantStatsListView,
    DeletePitomnikPlantView,
    DownloadPitomnikPlants,
    ListPitomnikPlantImage,
    OrganizationPitomnikPlantStatsListView,
    PitomnikPlantCreateView,
    PitomnikPlantListView,
    RepublicPitomnikPlantListView,
    UpdatePitomnikPlantView,
    DownloadPlantedPlantss
)
from .views.pitomnik_saving_job import (
    CreatePitomnikSavingJob,
    DeletePitomnikSavingJob,
    ListPitomnikSavingJob,
    ListPitomnikSavingJobImages,
    UpdatePitomnikSavingJob,
)
from .views.saving_job import (
    CreateSavingJobView,
    DeleteSavingJobView,
    AdminDeleteSavingJobView,
    DownloadSavingJobView,
    ListSavingJobAdminView,
    ListSavingJobByOrganizationAdmin,
    ListSavingJobImages,
    ListSavingJobView,
    UpdateSavingJobView,
    UpdateAdminSavingJobView,
)

app_name = "pitomnik"

landscapejob_urls = [
    path("", ListLandScapeJob.as_view(), name="list"),
    path("add/", CreateLandScapeJob.as_view(), name="add"),
    path("<int:pk>/change/", UpdateLandScapeJob.as_view(), name="change"),
    path("<int:pk>/change_admin/", AdminUpdateLandScapeJob.as_view(), name="change_for_admin"),
    path("<int:pk>/delete/", DeleteLandScapeJob.as_view(), name="delete"),
    path("<int:pk>/delete_admin/", AdminDeleteLandScapeJob.as_view(), name="delete_for_admin"),
    path("admin/", ListLandScapeJobAdmin.as_view(), name="list_admin"),
    path(
        "region/<int:pk>/landscape/",
        ListLandScapeJobByOrganizationAdmin.as_view(),
        name="list_region_admin",
    ),
    path("<int:id>/images/", ListLandScapeJobImages.as_view(), name="images"),
]

pitomnik_urls = [
    path("", ListPitomnikView.as_view(), name="list"),
    path("<int:id>/", AdminListPitomnikView.as_view(), name="admin_list"),
    path("add/", CreatePitomnikView.as_view(), name="add"),
    path("<int:pk>/change/", UpdatePitomnikView.as_view(), name="change"),
    path("<int:pk>/delete/", DeletePitomnikView.as_view(), name="delete"),
    path("<int:id>/images/", ListPitomnikImages.as_view(), name="images"),
]

pitomnikplants_urls = [
    path("add/", PitomnikPlantCreateView.as_view(), name="add"),
    path("", PitomnikPlantListView.as_view(), name="list"),
    path("admin/", AdminPitomnikPlantListView.as_view(), name="admin_list"),
    path(
        "stats/organization/",
        OrganizationPitomnikPlantStatsListView.as_view(),
        name="pitomnik-plants-of-an-organization",
    ),
    path(
        "<int:pk>/change/",
        UpdatePitomnikPlantView.as_view(),
        name="change",
    ),
    path(
        "<int:pk>/delete/",
        DeletePitomnikPlantView.as_view(),
        name="delete",
    ),
    path(
        "<int:id>/images/",
        ListPitomnikPlantImage.as_view(),
        name="images",
    ),
    path(
        "stats/admin/<int:pk>/",
        AdminPitomnikPlantStatsListView.as_view(),
        name="admin-stats-by-organization",
    ),
    path(
        "stats/republic",
        RepublicPitomnikPlantListView.as_view(),
        name="republic-pitomnik-plants",
    ),
    path(
        "download/",
        DownloadPlantedPlantss.as_view(),
        name="download",
    ),
]
irrigation_urls = [
    path("add/", CreateIrrigationView.as_view(), name="add"),
    path("", IrrigationFilteredListView.as_view(), name="list"),
    path("<int:pk>/change/", UpdateIrrigationView.as_view(), name="change"),
    path("<int:pk>/change_admin/", AdminUpdateIrrigationView.as_view(), name="change_for_admin"),
    path("<int:pk>/delete/", DeleteIrrigationView.as_view(), name="delete"),
    path("<int:pk>/delete_admin/", AdminDeleteIrrigationView.as_view(), name="delete_for_admin"),
    path(
        "admin/", IrrigationFilteredListViewAdmin.as_view(), name="list_admin"
    ),
    path(
        "organization/<int:pk>/irrigation/",
        IrrigationAdminByOrganization.as_view(),
        name="list_region_admin",
    ),
    path(
        "<int:id>/images/",
        ListIrrigationImages.as_view(),
        name="images",
    ),
]

planted_plant_urls = [
    path("add/", CreatePlantedPlant.as_view(), name="add"),
    path("<int:pk>/delete", DeletePlantedPlant.as_view(), name="delete"),
    path("change/<int:pk>", UpdateListPlantedPlantView.as_view(), name="change"),
    path("ajax/plants/", LoadPlantView.as_view(), name="ajax_plant_list"),
    path(
        "ajax/districts/",
        LoadDistrictView.as_view(),
        name="ajax_district_list",
    ),
    path("", ListPlantedPlantView.as_view(), name="list"),
    path("<int:pk>/", AdminListPlantedPlantView.as_view(), name="admin_list"),
    path("ajax/roads/", LoadRoadView.as_view(), name="ajax_road_list"),
    path(
        "region/statistics/",
        ListPlantedPlantByRoadView.as_view(),
        name="road_statistics",
    ),
    path(
        "republic/statistics/",
        ListPlantedPlantByRegionAdminView.as_view(),
        name="republic_statistics",
    ),
    path(
        "region/<int:pk>/statistics/",
        ListPlantedPlantByRoadAdminView.as_view(),
        name="admin_road_statistics",
    ),
    path("<int:id>/images/", ListPlantedPlantImage.as_view(), name="images"),
    path("download/", DownloadPlantedPlant.as_view(), name="download"),
]
plant_urls = [
    path("", ListPlantView.as_view(), name="list"),
    path("add/", CreatePlantView.as_view(), name="add"),
    path("<int:pk>/change/", UpdatePlantView.as_view(), name="change"),
    path("<int:pk>/delete/", DeletePlantView.as_view(), name="delete"),
]

saving_job_urls = [
    path("add/", CreateSavingJobView.as_view(), name="add"),
    path("<int:pk>/change/", UpdateSavingJobView.as_view(), name="change"),
    path("<int:pk>/change_admin/", UpdateAdminSavingJobView.as_view(), name="change_for_admin"),
    path("<int:pk>/delete/", DeleteSavingJobView.as_view(), name="delete"),
    path("<int:pk>/delete_admin/", AdminDeleteSavingJobView.as_view(), name="delete_for_admin"),
    path("", ListSavingJobView.as_view(), name="list"),
    path("admin/", ListSavingJobAdminView.as_view(), name="list_admin"),
    path(
        "region/<int:pk>/savingjob",
        ListSavingJobByOrganizationAdmin.as_view(),
        name="list_region_admin",
    ),
    path(
        "download/<int:pk>/", DownloadSavingJobView.as_view(), name="download"
    ),
    path(
        "<int:id>/images/",
        ListSavingJobImages.as_view(),
        name="images",
    ),
]

new_irrigation_urls = [
    path("", ListNewIrrigationView.as_view(), name="list"),
    path("add/", CreateNewIrrigationView.as_view(), name="add"),
    path("<int:pk>/change/", UpdateNewIrrigationView.as_view(), name="change"),
    path("<int:pk>/change_admin/", AdminUpdateNewIrrigationView.as_view(), name="change_for_admin"),
    path("<int:pk>/delete/", DeleteNewIrrigationView.as_view(), name="delete"),
    path("<int:pk>/delete_admin/", AdminDeleteNewIrrigationView.as_view(), name="delete_for_admin"),
    path("admin/", ListNewIrrigationAdminView.as_view(), name="list_admin"),
    path(
        "region/<int:pk>/",
        ListNewIrrigationByOrganizationAdmin.as_view(),
        name="list_region_admin",
    ),
    path(
        "<int:id>/images/",
        ListNewIrrigationImages.as_view(),
        name="images",
    ),
]

pitomnik_saving_job = [
    path("", ListPitomnikSavingJob.as_view(), name="list"),
    path("add/", CreatePitomnikSavingJob.as_view(), name="add"),
    path("<int:pk>/change/", UpdatePitomnikSavingJob.as_view(), name="change"),
    path("<int:pk>/delete/", DeletePitomnikSavingJob.as_view(), name="delete"),
    path(
        "<int:id>/images/",
        ListPitomnikSavingJobImages.as_view(),
        name="images",
    ),
]

road_add_urls = [
    path('', road_add, name='road_add'),
    path('form/', road_add_form, name='road_add_form'),
    path('delete/<int:pk>/', road_delete, name='road_delete'),
    path('change/<int:pk>/', road_change, name='road_change'),
]

urlpatterns = [
    path("pitomnik/", include((pitomnik_urls, "pitomnik"))),
    path("pitomnikplants/", include((pitomnikplants_urls, "pitomnikplants"))),
    path("plantedplants/", include((planted_plant_urls, "plantedplants"))),
    path("plant/", include((plant_urls, "plant"))),
    path("irrigation/", include((irrigation_urls, "irrigation"))),
    path("savingjob/", include((saving_job_urls, "savingjob"))),
    path("map/", index, name="map"),
    path('add_road/', include(road_add_urls)),
    path("landscapejob/", include((landscapejob_urls, "landscapejob"))),
    path("newirrigation/", include((new_irrigation_urls, "newirrigation"))),
    path(
        "pitomniksavingjob/",
        include((pitomnik_saving_job, "pitomniksavingjob")),
    ),
]
