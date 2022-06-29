from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.views.generic.base import View
from django_filters.views import FilterView
from ..filters import PitomnikFilter, PitomnikPlantFilter
from ..forms import PitomnikPlantForm, PitomnikPlantImageFormSet
from ..models import Pitomnik, PitomnikPlantImage, PitomnikPlants
from utils.download_file import download_1
from datetime import date


class PitomnikPlantListView(PermissionRequiredMixin, FilterView):
    permission_required = "pitomnik.view_pitomnikplants"
    paginate_by = settings.PITOMNIK_PLANTS_PAGE_SIZE
    template_name = "pitomnik/pitomnik_plants/list.html"
    filterset_class = PitomnikFilter

    def get_queryset(self):
        return PitomnikPlants.objects.get_plants_by_organization(
            self.request.user.organization
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        for x in context['object_list']:
            print(x.plant)
        print(context)
        plant_type = self.request.GET.get('plant__type')
        total = PitomnikPlants.objects.get_total_statistics(
            self.request.user.organization, plant_type
        )
        context["total_plant"] = total[0]["total_plant"]

        return context

    def get_filterset_kwargs(self, filterset_class):
        kwargs = super(PitomnikPlantListView, self).get_filterset_kwargs(
            filterset_class
        )
        kwargs["organization"] = self.request.user.organization
        return kwargs


class AdminPitomnikPlantListView(PermissionRequiredMixin, FilterView):
    permission_required = "pitomnik.view_pitomnikplants_admin"
    paginate_by = settings.PITOMNIK_PLANTS_PAGE_SIZE
    template_name = "pitomnik/pitomnik_plants/admin_list.html"
    queryset = PitomnikPlants.objects.get_plant_and_pitomnik_and_organization()
    filterset_class = PitomnikPlantFilter
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        plant_type = self.request.GET.get('plant__type')
        total = PitomnikPlants.objects.get_total_statistics(
            self.request.user.organization, plant_type
        )
        context["total_plant"] = total[0]["total_plant"]
        context['pitomnik__organization'] = self.request.GET.get('pitomnik__organization')
        context['pitomnik'] = self.request.GET.get('pitomnik')
        context['plant'] = self.request.GET.get('plant')
        context['plant__type'] = self.request.GET.get('plant__type')
        context['status'] = self.request.GET.get('status')
        return context


class PitomnikPlantCreateView(PermissionRequiredMixin, CreateView):
    permission_required = "pitomnik.add_pitomnikplants"
    model = PitomnikPlants
    template_name = "pitomnik/pitomnik_plants/add.html"
    success_url = reverse_lazy("pitomnik:pitomnikplants:list")
    form_class = PitomnikPlantForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["images"] = PitomnikPlantImageFormSet(
                self.request.POST, self.request.FILES
            )
        else:
            data["images"] = PitomnikPlantImageFormSet()
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


class UpdatePitomnikPlantView(PermissionRequiredMixin, UpdateView):
    permission_required = "pitomnik.change_pitomnikplants"
    model = PitomnikPlants
    template_name = "pitomnik/pitomnik_plants/add.html"
    success_url = reverse_lazy("pitomnik:pitomnikplants:list")
    form_class = PitomnikPlantForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["images"] = PitomnikPlantImageFormSet(
                self.request.POST, self.request.FILES, instance=self.object
            )
        else:
            data["images"] = PitomnikPlantImageFormSet(instance=self.object)
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


class AdminPitomnikPlantStatsListView(PermissionRequiredMixin, ListView):
    permission_required = "pitomnik.view_pitomnikplants_admin"
    paginate_by = settings.PITOMNIK_PLANTS_PAGE_SIZE
    template_name = "pitomnik/pitomnik_plants/stats.html"
    context_object_name = "pitomnik_plant_stats"

    def get_queryset(self):
        organization = self.kwargs["pk"]
        plant_type = self.request.GET.get("type")
        return PitomnikPlants.objects.pitomnik_plant_stats(
            organization, plant_type
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context["pk"] = self.kwargs.get("pk")
        plant_type = self.request.GET.get("type")
        if plant_type is None:
            plant_type = ""
        context["section"] = plant_type
        total = PitomnikPlants.objects.get_total_statistics(
            self.kwargs["pk"], plant_type
        )
        context["total_plant"] = total[0]["total_plant"]
        context["total_ready_plant"] = total[1]["total_ready_plant"]
        context["total_field"] = total[2]["total_field_to_be_planted"]
        return context


class OrganizationPitomnikPlantStatsListView(
    PermissionRequiredMixin, ListView
):
    permission_required = "pitomnik.view_pitomnikplants"
    paginate_by = settings.PITOMNIK_PLANTS_PAGE_SIZE
    template_name = "pitomnik/pitomnik_plants/groupped_list.html"
    context_object_name = "pitomnik_plant_stats"

    def get_queryset(self):
        plant_type = self.request.GET.get("type")
        return PitomnikPlants.objects.pitomnik_plant_stats(
            self.request.user.organization, plant_type
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        plant_type = self.request.GET.get("type")
        if plant_type is None:
            plant_type = ""
        context["section"] = plant_type
        total = PitomnikPlants.objects.get_total_statistics(
            self.request.user.organization, plant_type
        )
        context["total_plant"] = total[0]["total_plant"]
        context["total_ready_plant"] = total[1]["total_ready_plant"]
        context["total_field"] = total[2]["total_field_to_be_planted"]
        return context


class RepublicPitomnikPlantListView(PermissionRequiredMixin, ListView):
    permission_required = "pitomnik.view_pitomnikplants_admin"
    paginate_by = settings.PITOMNIK_PLANTS_PAGE_SIZE
    template_name = "pitomnik/pitomnik_plants/groupped_republic.html"
    context_object_name = "pitomnik_plant_republic"

    def get_queryset(self):
        plant_type = self.request.GET.get("type")
        return PitomnikPlants.objects.pitomnik_plant_stats(
            organization=None,
            plant_type=plant_type,
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        plant_type = self.request.GET.get("type")
        if plant_type is None:
            plant_type = ""
        context["section"] = plant_type
        total = PitomnikPlants.objects.get_total_statistics(
            organization=None, plant_type=plant_type
        )
        context["total_plant"] = total[0]["total_plant"]
        context["total_ready_plant"] = total[1]["total_ready_plant"]
        context["total_field"] = total[2]["total_field_to_be_planted"]
        return context


class DeletePitomnikPlantView(PermissionRequiredMixin, DeleteView):
    permission_required = ["pitomnik.delete_pitomnik"]
    model = PitomnikPlants
    success_url = reverse_lazy("pitomnik:pitomnikplants:list")

    def get_success_url(self):
        return self.request.META.get("HTTP_REFERER")


class ListPitomnikPlantImage(PermissionRequiredMixin, ListView):
    permission_required = "pitomnik.view_pitomnikplantimage"
    template_name = "pitomnik/pitomnik_plants/images.html"

    def get_queryset(self):
        return PitomnikPlantImage.objects.filter_by_pitomnik_plant(
            self.kwargs["id"], self.request.user
        )


class DownloadPitomnikPlants(View):
    def get(self, *args, **kwargs):
        pitomnik_plants = Pitomnik.objects.pitomnik_for_excel()
        pitomnik_plants = pitomnik_plants.values_list(
            "name",
            "area",
            "total_quantity",
            "seed_quantity",
            "sprout_quantity",
            "ready_quantity",
        )
        data = list(pitomnik_plants)
        db = ""
        for x in data:
            db += str(x) + "\n"
        with open("db_list", "w+") as f:

            f.write(str(db))
        data_clone = []
        for row in data:
            data_clone.append(row[1:])
        row_total = ["Жами"] + list(map(sum, zip(*data_clone)))
        data.append(row_total)
        path = "pitomnik_plant"
        row_start_index = 4
        column_start_index = 1
        column_end_range = 7
        indexing = True
        return download_1(
            data,
            path,
            row_start_index,
            column_start_index,
            column_end_range,
            indexing,
        )


class DownloadPlantedPlantss(View):
    def get(self, url, *args, **kwargs):
        pitomnik__organization_po = url.GET.get("pitomnik__organization")
        pitomnik_pk = url.GET.get("pitomnik")
        plant_pl = url.GET.get("plant")
        plant__type_pt = url.GET.get("plant__type")
        status_st = url.GET.get("status")
        pitomnik_plants = PitomnikPlants.objects.get_pitomnik_plant_for_excel()
        if status_st == "ready":
            status_st = "Тайёр"
        elif status_st == "not_ready":
            status_st = "Тайёр эмас"

        _list_pitomnikdb = []
        for x in pitomnik_plants:
            def status(dt):
                if dt <= date.today():
                    return "Тайёр"
                else:
                    return "Тайёр эмас"

            pitomnik__organization = pitomnik__organization_po
            pitomnik = pitomnik_pk
            plant = plant_pl
            plant__type = plant__type_pt
            status_st = ""
            if not str(pitomnik__organization).isdigit():
                pitomnik__organization = x.pitomnik.organization.id
            else:
                pitomnik__organization = int(pitomnik__organization)
            if not str(pitomnik).isdigit():
                pitomnik = x.pitomnik.id
            else:
                pitomnik = int(pitomnik)
            if not str(plant).isdigit():
                plant = x.plant.id
            else:
                plant = int(plant)
            if str(plant__type) == "" or str(plant__type) == "None":
                plant__type = x.plant.type
            if not status_st or str(status_st) == "None":
                status_st = status(x.readiness_date)
            print(0)
            if pitomnik__organization == x.pitomnik.organization.id and pitomnik == x.pitomnik.id and plant == x.plant.id and str(plant__type) == str(x.plant.type) and (status(x.readiness_date)) == status_st:
                if x.plant.type == "BUSH":
                    x.plant.type = "Бута"
                elif x.plant.type == "LEAF_SHAPED":
                    x.plant.type = "Япрок баргли"
                elif x.plant.type == "CONIFEROUS":
                    x.plant.type = "Игна Баргли"


                if x.readiness_date <= date.today():
                    status = "Тайёр"
                else:
                    status = "Тайёр эмас"
                _list_pitomnikdb.append(tuple((str(x.pitomnik.organization.name), str(x.pitomnik.name), str(x.plant),
                                               str(x.plant.type), str(x.quantity), str(x.dried), str(x.plant_field),
                                               str(x.planted_date), str(x.changed_at), status)))
            else:
                pitomnik__organization = int(pitomnik__organization)
            if not str(pitomnik).isdigit():
                pitomnik = x.pitomnik.id
            else:
                pitomnik = int(pitomnik)
            if not str(plant).isdigit():
                plant = x.plant.id
            else:
                plant = int(plant)
            if str(plant__type) == "" or str(plant__type) == "None":
                plant__type = x.plant.type

            if not status_st or str(status_st) == "None":
                status_st = status(x.readiness_date)
            if pitomnik__organization == x.pitomnik.organization.id and pitomnik == x.pitomnik.id and plant == x.plant.id and str(plant__type) == str(x.plant.type) and (status(x.readiness_date)) == status_st:
                if x.plant.type == "BUSH":
                    x.plant.type = "Бута"
                elif x.plant.type == "LEAF_SHAPED":
                    x.plant.type = "Япрок баргли"
                elif x.plant.type == "CONIFEROUS":
                    x.plant.type = "Игна Баргли"
                if x.readiness_date <= date.today():
                    status = "Тайёр"
                else:
                    status = "Тайёр эмас"
                _list_pitomnikdb.append(tuple((str(x.pitomnik.organization.name), str(x.pitomnik.name), str(x.plant),
                                               str(x.plant.type), str(x.quantity), str(x.dried), str(x.plant_field),
                                               str(x.planted_date), str(x.changed_at), status)))
        path = "pitomnik_plant"
        row_start_index = 4
        column_start_index = 1
        column_end_range = 11
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
