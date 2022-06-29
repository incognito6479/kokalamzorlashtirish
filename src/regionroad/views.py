import json
import os

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse, JsonResponse
from django.urls import reverse_lazy
from django.views import View, generic

from django_filters.views import FilterView

from config.settings.base import BASE_DIR
from pitomnik.base_mixin import BaseMixin
from regionroad.filters import RoadFilter
from regionroad.forms import RoadDistrictForm
from regionroad.models import District, Region, RoadDistrict


class GetJson(View):
    @login_required
    def get(self, request):
        with open(
            os.path.join(BASE_DIR, "regionroad/csv_data/cities.json")
        ) as f:
            data = json.load(f)
            return JsonResponse(data)


class RoadDistrictCreateView(
    PermissionRequiredMixin, BaseMixin, generic.CreateView
):
    model = RoadDistrict
    template_name = "road_district/create.html"
    form_class = RoadDistrictForm
    success_url = reverse_lazy("regionroad:road-district-list")
    permission_required = [
        "regionroad.add_roaddistrict",
    ]


class RoadDistrictListView(PermissionRequiredMixin, FilterView):
    permission_required = "regionroad.view_roaddistrict"
    template_name = "road_district/list.html"
    paginate_by = settings.DISTRICT_ROAD_PAGE_SIZE
    queryset = RoadDistrict.objects.get_road_district()
    filterset_class = RoadFilter


class RoadDistrictUpdateView(PermissionRequiredMixin, generic.UpdateView):
    model = RoadDistrict
    template_name = "road_district/update.html"
    form_class = RoadDistrictForm
    success_url = reverse_lazy("regionroad:road-district-list")
    permission_required = [
        "regionroad.change_roaddistrict",
    ]


class RoadDistrictDeleteView(PermissionRequiredMixin, generic.DeleteView):
    model = RoadDistrict
    template_name = "road_district/update.html"
    success_url = reverse_lazy("regionroad:road-district-list")
    permission_required = [
        "regionroad.delete_roaddistrict",
    ]


class GetRegions(View):
    def get(self, request):
        data = serializers.serialize("json", queryset=Region.objects.all())
        return HttpResponse(data, content_type="application/json")


class GetRegionDistrict(View):
    def get(self, request, pk):
        # print(pk)
        data = serializers.serialize(
            "json", queryset=District.objects.filter_by_region(pk)
        )
        return HttpResponse(data, content_type="application/json")

    class GetRegionRoad(View):
        pass


class GetRegionPlantQuantity(View):
    def get(self, request, pk):
        # print(pk)
        data = json.dumps(
            list(
                RoadDistrict.objects.get_plantedplants_quantity_by_region(pk)
            ),
            cls=DjangoJSONEncoder,
        )
        # print(data)
        return HttpResponse(data, content_type="application/json")


class GetDistrictPlantQuantity(View):
    def get(self, request, pk):
        data = json.dumps(
            list(
                RoadDistrict.objects.get_plantedplants_quantity_by_district(pk)
            ),
            cls=DjangoJSONEncoder,
        )
        return HttpResponse(data, content_type="application/json")


class GetRepublicPlantQuantity(View):
    def get(self, request):
        data = json.dumps(
            RoadDistrict.objects.get_plantedplants_quantity_republic(),
            cls=DjangoJSONEncoder,
        )
        return HttpResponse(data, content_type="application/json")


class GetUzbJson(View):
    def get(self, request):
        f = open(os.path.join(BASE_DIR, "regionroad/csv_data/uzb.json"), "r")
        return HttpResponse(f, content_type="application/json")
