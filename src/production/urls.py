from django.urls import include, path

from .views import (
    CreateIrrigationProduction,
    CreateLandscapeJobProduction,
    CreateMonthlyProdView,
    CreatePlantingProduction,
    CreateSavingJobProduction,
    CreateYearlyProdView,
    DeleteIrrigationView,
    DeleteLandScapeJobProductionView,
    DeleteMonthlyProdView,
    DeletePlantingProductionView,
    DeleteSavingJobProductionView,
    DeleteYearlyProdView,
    DownloadProductionView,
    IrrigationProductionListView,
    LandscapeJobProductionListView,
    ListMonthlyProdPlanAJAX,
    ListMonthProdView,
    ListYearLyProdPlanAJAX,
    ListYearlyProdView,
    PlantingProductionListView,
    SavingProductionListView,
    StatByOrganizationAndYear,
    StatByOrganizationAndYearRoadType,
    UpdateIrrigationProduction,
    UpdateLandScapeJobProduction,
    UpdateMonthlyProdView,
    UpdatePlantingProduction,
    UpdateSavingJobProduction,
    UpdateYearlyProdView,
)

app_name = "production"
api_urls = [
    path("months/", ListMonthlyProdPlanAJAX.as_view(), name="months"),
    path("years/", ListYearLyProdPlanAJAX.as_view(), name="years"),
]
irrigation_urls = [
    path("list/", IrrigationProductionListView.as_view(), name="list"),
    path("create/", CreateIrrigationProduction.as_view(), name="create"),
    path(
        "<int:pk>/change/", UpdateIrrigationProduction.as_view(), name="change"
    ),
    path("<int:pk>/delete/", DeleteIrrigationView.as_view(), name="delete"),
]
saving_urls = [
    path("list/", SavingProductionListView.as_view(), name="list"),
    path("create/", CreateSavingJobProduction.as_view(), name="create"),
    path(
        "<int:pk>/change/", UpdateSavingJobProduction.as_view(), name="change"
    ),
    path(
        "<int:pk>/delete/",
        DeleteSavingJobProductionView.as_view(),
        name="delete",
    ),
]
planting_urls = [
    path("list/", PlantingProductionListView.as_view(), name="list"),
    path("create/", CreatePlantingProduction.as_view(), name="create"),
    path(
        "<int:pk>/change/", UpdatePlantingProduction.as_view(), name="change"
    ),
    path(
        "<int:pk>/delete/",
        DeletePlantingProductionView.as_view(),
        name="delete",
    ),
]
landscape_urls = [
    path("list/", LandscapeJobProductionListView.as_view(), name="list"),
    path("create/", CreateLandscapeJobProduction.as_view(), name="create"),
    path(
        "<int:pk>/change/",
        UpdateLandScapeJobProduction.as_view(),
        name="change",
    ),
    path(
        "<int:pk>/delete/",
        DeleteLandScapeJobProductionView.as_view(),
        name="delete",
    ),
]
yearly_urls = [
    path("list/", ListYearlyProdView.as_view(), name="list"),
    path("create/", CreateYearlyProdView.as_view(), name="create"),
    path("<int:pk>/change/", UpdateYearlyProdView.as_view(), name="change"),
    path("<int:pk>/delete/", DeleteYearlyProdView.as_view(), name="delete"),
]

monthly_urls = [
    path("create/", CreateMonthlyProdView.as_view(), name="create"),
    path("list/", ListMonthProdView.as_view(), name="list"),
    path("<int:pk>/change/", UpdateMonthlyProdView.as_view(), name="change"),
    path("<int:pk>/delete/", DeleteMonthlyProdView.as_view(), name="delete"),
]

stat_urls = [
    path("organization/", StatByOrganizationAndYear.as_view(), name="stat"),
    path(
        "republic/",
        StatByOrganizationAndYearRoadType.as_view(),
        name="stat_republic",
    ),
    path(
        "republic/download/",
        DownloadProductionView.as_view(),
        name="download",
    ),
]

urlpatterns = [
    path("irrigation/", include((irrigation_urls, "irrigation"))),
    path("saving/", include((saving_urls, "saving"))),
    path("planting/", include((planting_urls, "planting"))),
    path("landscape/", include((landscape_urls, "landscape"))),
    path("yearly/", include((yearly_urls, "yearly"))),
    path("monthly/", include((monthly_urls, "monthly"))),
    path("stat/", include((stat_urls, "stat"))),
    path("api/", include((api_urls, "api"))),
]
