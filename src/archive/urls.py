from django.conf.urls import include
from django.urls import path

from archive.views import ListSaving

app_name = "archive"

saving_urls = [
    path("", ListSaving.as_view(), name="list"),
]

urlpatterns = [
    path("saving/", include((saving_urls, "saving"))),
]
