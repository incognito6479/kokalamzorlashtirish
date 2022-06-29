from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.views.generic.base import View
from datetime import date
from django.db.models import Sum
from django_filters.views import FilterView
from account.models import Organization
from pitomnik.filters import PlantedPlantFilter
from pitomnik.forms import PlantedPlantForm, PlantedPlantImageFormSet
from pitomnik.models import PitomnikPlants, PlantedPlantImage, PlantedPlants
from regionroad.models import District, Region, RoadDistrict
from utils.download_file import download, download_1
from regionroad.models import District, Region, RoadDistrict, Road
from utils.download_file import download, download_1
from datetime import date


class CreatePlantedPlant(PermissionRequiredMixin, CreateView):
    template_name = "pitomnik/planted_plant/add.html"
    permission_required = ("pitomnik.add_plantedplants",)
    model = PlantedPlants
    success_url = reverse_lazy("pitomnik:plantedplants:list")
    form_class = PlantedPlantForm

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["images"] = PlantedPlantImageFormSet(
                self.request.POST, self.request.FILES
            )
        else:
            data["images"] = PlantedPlantImageFormSet()
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        images = context["images"]
        with transaction.atomic():
            form.instance.added_by = self.request.user
            form.instance.organization = self.request.user.organization
            self.object = form.save()
            if images.is_valid():
                images.instance = self.object
                images.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class LoadPlantView(PermissionRequiredMixin, ListView):
    template_name = "pitomnik/planted_plant/ajax_plant.html"
    permission_required = "pitomnik.view_pitomnikplants"

    def get_queryset(self):
        pitomnik_id = self.request.GET.get("pitomnik")
        return PitomnikPlants.objects.get_plants(pitomnik_id)


class LoadDistrictView(ListView):
    template_name = "pitomnik/planted_plant/ajax_list.html"

    def get_queryset(self):
        region_id = self.request.GET.get("region")
        return District.objects.filter_by_region(region_id)


class LoadRoadView(ListView):
    template_name = "pitomnik/planted_plant/ajax_road.html"

    def get_queryset(self):
        district_id = self.request.GET.get("district")
        return RoadDistrict.objects.filter_by_district(district_id)


class ListPlantedPlantView(PermissionRequiredMixin, FilterView):
    permission_required = "pitomnik.view_plantedplants"
    paginate_by = settings.PLANTED_PLANTS_PAGE_SIZE
    template_name = "pitomnik/planted_plant/list.html"
    filterset_class = PlantedPlantFilter

    def get_queryset(self):
        return PlantedPlants.objects.get_planted_plants(
            self.request.user.organization
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['district'] = self.request.GET.get('road_district__district')
        context['road_district'] = self.request.GET.get('road_district__road')
        context['plant'] = self.request.GET.get('plant')
        t = 0
        for i in PlantedPlants.objects.get_planted_plants(self.request.user.organization):
            t += int(i.quantity)
        context['total_'] = t
        return context


class UpdateListPlantedPlantView(PermissionRequiredMixin, UpdateView):
    permission_required = "pitomnik.change_plantedplants"
    model = PlantedPlants
    template_name = "pitomnik/planted_plant/add.html"
    success_url = reverse_lazy("pitomnik:plantedplants:list")
    form_class = PlantedPlantForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["images"] = PlantedPlantImageFormSet(
                self.request.POST, self.request.FILES, instance=self.object
            )
        else:
            data["images"] = PlantedPlantImageFormSet(instance=self.object)
        d = PlantedPlants.objects.get(id=self.kwargs['pk'])
        a = RoadDistrict.objects.get(id=d.road_district_id)
        if d.pitomnik_id:
            data['pitomnik'] = str(d.pitomnik_id)
        data['plant'] = str(d.plant_id)
        data['district'] = str(a.district_id)
        data['quantity'] = str(d.quantity)
        data['road_id'] = str(a.id)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        form.instance.id = context['plantedplants'].id
        images = context["images"]
        with transaction.atomic():
            form.instance.added_by = self.request.user
            form.instance.organization = self.request.user.organization
            self.object = form.save()
            if images.is_valid():
                images.instance = self.object
                images.save()
        return super().form_valid(form)


class AdminListPlantedPlantView(ListPlantedPlantView):
    permission_required = "pitomnik.view_plantedplants_admin"
    template_name = "pitomnik/planted_plant/admin_list.html"

    def get_queryset(self):
        return PlantedPlants.objects.get_planted_plants(self.kwargs["pk"])


class ListPlantedPlantByRoadView(PermissionRequiredMixin, ListView):
    permission_required = "pitomnik.view_plantedplants"
    paginate_by = settings.PLANTED_PLANTS_PAGE_SIZE
    template_name = "pitomnik/statistics/planted_plant_by_region.html"

    def get_queryset(self):
        region = self.request.user.organization.region
        return RoadDistrict.objects.get_planted_plants(region)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        region = self.request.user.organization.region
        context["road_type"] = RoadDistrict.objects.get_by_road_type(region)
        context[
            "region_all"
        ] = RoadDistrict.objects.get_plantedplants_quantity_region(region)
        return context


class ListPlantedPlantByRegionAdminView(PermissionRequiredMixin, ListView):
    permission_required = "pitomnik.view_plantedplants_admin"
    template_name = "pitomnik/statistics/planted_plant_by_region_admin.html"

    def get_queryset(self):
        return RoadDistrict.objects.get_by_region()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context["region_list"] = RoadDistrict.objects.get_regions_total_stat()
        context["republic_sum"] = RoadDistrict.objects.get_all_statistics()
        context[
            "republic_by_road_type"
        ] = RoadDistrict.objects.get_republic_stat_by_road_type()
        r = Region.objects.all()
        rd = RoadDistrict.objects.all()
        dict_to_send = {}
        total_to_send = {}
        total_send_for_republic = {}
        for i in r:
            dict_to_send[i.id] = [
                {1: rd.filter(district_id__region_id=i.id, road_id__road_type=1).aggregate(Sum('requirement'))},
                {2: rd.filter(district_id__region_id=i.id, road_id__road_type=2).aggregate(Sum('requirement'))},
                {3: rd.filter(district_id__region_id=i.id, road_id__road_type=3).aggregate(Sum('requirement'))}
            ]
            total_to_send[i.id] = rd.filter(district_id__region_id=i.id).aggregate(Sum('requirement'))
        total_send_for_republic[1] = rd.filter(road_id__road_type=1).aggregate(Sum('requirement'))
        total_send_for_republic[2] = rd.filter(road_id__road_type=2).aggregate(Sum('requirement'))
        total_send_for_republic[3] = rd.filter(road_id__road_type=3).aggregate(Sum('requirement'))

        context['dict_to_send'] = dict_to_send
        context['total_to_send'] = total_to_send
        context['total_send_for_republic'] = total_send_for_republic
        return context


class ListPlantedPlantByRoadAdminView(ListPlantedPlantByRoadView):
    permission_required = "pitomnik.view_plantedplants_admin"

    def get_queryset(self):
        region = get_object_or_404(Region, pk=self.kwargs["pk"])
        return RoadDistrict.objects.get_planted_plants(region)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        region = get_object_or_404(Region, pk=self.kwargs["pk"])
        context["road_type"] = RoadDistrict.objects.get_by_road_type(region)
        context[
            "region_all"
        ] = RoadDistrict.objects.get_plantedplants_quantity_region(region)
        rd = RoadDistrict.objects.all()
        rd = rd.filter(district_id__region_id=region)
        total_send_for_region = {}
        total_send_for_region[1] = rd.filter(road_id__road_type=1).aggregate(Sum('requirement'))
        total_send_for_region[2] = rd.filter(road_id__road_type=2).aggregate(Sum('requirement'))
        total_send_for_region[3] = rd.filter(road_id__road_type=3).aggregate(Sum('requirement'))
        total_show = rd.aggregate(Sum('requirement'))
        print(total_send_for_region)
        print(total_show)
        context['t'] = total_send_for_region
        context['total'] = total_show
        return context


class ListPlantedPlantImage(PermissionRequiredMixin, ListView):
    permission_required = "pitomnik.view_plantedplantimage"
    template_name = "pitomnik/planted_plant/images.html"

    def get_queryset(self):
        return PlantedPlantImage.objects.filter_by_planted_plant(
            self.kwargs["id"]
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        planted_plant = PlantedPlants.objects.get(pk=self.kwargs["id"])
        organization = planted_plant.added_by.organization
        context["organization"] = organization
        return context


class DeletePlantedPlant(PermissionRequiredMixin, DeleteView):
    permission_required = ["pitomnik.delete_plantedplants"]
    model = PlantedPlants

    def get_success_url(self):
        return self.request.META.get("HTTP_REFERER")


class DownloadPlantedPlant(View):
    def get(self, url, *args, **kwargs):
        district_dt = int(url.GET.get("district")) if url.GET.get("district").isdigit() else ""
        road_district_rd = int(url.GET.get("road_district")) if url.GET.get("road_district").isdigit() else ""
        plant_pt = int(url.GET.get("plant")) if url.GET.get("plant").isdigit() else ""
        pitomnik_plants = PlantedPlants.objects.get_planted_plants(
            self.request.user.organization
        )
        _list_pitomnikdb = []
        for x in pitomnik_plants:
            district = district_dt
            road_district = road_district_rd
            plant = plant_pt
            if not district:
                district = x.road_district.district.id

            if not road_district:
                road_district = x.road_district.road.id

            if not plant:
                plant = x.plant.id

            if district == x.road_district.district.id and road_district == x.road_district.road.id and plant == x.plant.id:
                _list_pitomnikdb.append(
                    tuple((str(x.road_district.district.name),
                           str(x.road_district.road.code) + " " + str(x.road_district.road.title),
                           "(" + str(int(x.road_from)) + "-" + str(int(x.road_to)) + ")km -" +  str(x.metr),
                           str(x.pitomnik.name if x.plant_source == 'PITOMNIK' else PlantedPlants.SourceType(x.plant_source).label),
                           "(" + str(int(x.road_from)) + "-" + str(int(x.road_to)) + ")km -" + str(x.metr),
                           str(x.pitomnik.name if x.plant_source == 'PITOMNIK' else PlantedPlants.SourceType(
                               x.plant_source).label),
                           str(x.plant.name),
                           str(x.quantity),
                           str(PlantedPlants.PlantingSide(x.planting_side).label),
                           str(x.planted_date))))

        path = "saving_plant"
        row_start_index = 4
        column_start_index = 1
        column_end_range = 9
        indexing = True
        db = list(_list_pitomnikdb)

        return download_1(
            _list_pitomnikdb,
            path,
            row_start_index,
            column_start_index,
            column_end_range,
            indexing,
        )