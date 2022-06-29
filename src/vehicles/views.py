from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.views.generic.base import View
from django.db.models import Count
from django_filters.views import FilterView

from account.models import Organization
from utils.download_file import download

from .filters import VehicleFilter
from .forms import VehicleAddForm, VehicleTypesForm, VehicleUpdateForm
from .models import Vehicle, VehicleTypes


class ListVehicleView(PermissionRequiredMixin, FilterView):
    permission_required = "vehicles.view_vehicle"
    paginate_by = settings.VEHICLE_PAGE_SIZE
    template_name = "vehicles/list.html"
    filterset_class = VehicleFilter

    def get_queryset(self):
        return Vehicle.objects.get_vehicle_with_regions(self.request.user).order_by('type__name')


class ListVehicleByOrganizationView(PermissionRequiredMixin, FilterView):
    permission_required = "vehicles.view_vehicle_admin"
    paginate_by = settings.VEHICLE_PAGE_SIZE
    template_name = "vehicles/list_by_organization.html"
    filterset_class = VehicleFilter

    def get_queryset(self):

        organization = get_object_or_404(Organization, pk=self.kwargs["pk"])
        # organization = Organization.objects.all()
        return Vehicle.objects.get_vehicle_by_organization(organization).order_by('type__name')

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data["organization"] = get_object_or_404(
            Organization, pk=self.kwargs["pk"]
        )
        return data


class ListVehicleAdminView(PermissionRequiredMixin, ListView):
    permission_required = "vehicles.view_vehicle_admin"
    paginate_by = settings.VEHICLE_PAGE_SIZE
    template_name = "vehicles/list_admin.html"

    def get_queryset(self):
        return Vehicle.objects.get_count_by_organization()


class CreateVehicleView(PermissionRequiredMixin, CreateView):
    permission_required = "vehicles.add_vehicle"
    model = Vehicle
    template_name = "vehicles/add.html"
    success_url = reverse_lazy("vehicles:local:list")
    form_class = VehicleAddForm

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        form.instance.organization = self.request.user.organization
        return super().form_valid(form)


class UpdateVehicleView(PermissionRequiredMixin, UpdateView):
    permission_required = "vehicles.change_vehicle"
    model = Vehicle
    template_name = "vehicles/add.html"
    success_url = reverse_lazy("vehicles:local:list")
    form_class = VehicleUpdateForm


class DeleteVehicleView(PermissionRequiredMixin, DeleteView):
    permission_required = "vehicles.delete_vehicle"
    model = Vehicle
    success_url = reverse_lazy("vehicles:local:list")
    template_name = "vehicles/list.html"


class CreateVehicleTypeView(PermissionRequiredMixin, CreateView):
    permission_required = "vehicles.view_vehicle_admin"
    model = VehicleTypes
    template_name = "vehicles/add_type.html"
    success_url = reverse_lazy("vehicles:admin:list_type")
    form_class = VehicleTypesForm

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        return super().form_valid(form)


class UpdateVehicleTypeView(PermissionRequiredMixin, UpdateView):
    permission_required = "vehicles.view_vehicle_admin"
    model = VehicleTypes
    template_name = "vehicles/add_type.html"
    success_url = reverse_lazy("vehicles:admin:list_type")
    form_class = VehicleTypesForm


class ListVehicleTypeView(PermissionRequiredMixin, ListView):
    permission_required = "vehicles.view_vehicle_admin"
    model = VehicleTypes
    template_name = "vehicles/list_type.html"
    paginate_by = settings.VEHICLE_PAGE_SIZE

    def get_queryset(self):
        return VehicleTypes.objects.all().order_by("-id")


class DownloadVehicleView(View):
    def get(self, request, *args, **kwargs):
        organization = Organization.objects.get(pk=self.kwargs["pk"])
        vehicle = Vehicle.objects.get_vehicle_by_organization(organization)
        vehicle = vehicle.values_list(
            "name",
            "manufactured_date",
            "registration_plate",
            "inventory",
            "balance_value",
            "aging_value",
            "mileage_value_start_year",
            "mileage_value_report_time",
            "GPS_status",
            "tech_state",
            "storage_site",
        )
        data = list(vehicle)
        path = "vehicle"
        row_start_index = 4
        column_start_index = 1
        column_end_range = 12
        indexing = True
        return download(
            data,
            path,
            row_start_index,
            column_start_index,
            column_end_range,
            indexing,
        )


class ListVehicleTypesCountByOrganization(PermissionRequiredMixin, ListView):
    permission_required = "vehicles.view_vehicle_admin"
    model = Vehicle
    template_name = "vehicles/list_by_type_organization.html"

    def get_queryset(self):
        return VehicleTypes.objects.all().order_by('id')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        t = Vehicle.objects.all().values('type_id').annotate(total=Count('type_id')).order_by('type_id')
        o = Vehicle.objects.filter(type_id=None)
        other = 0
        for i in o:
            other += 1
        context['t'] = t
        context['other'] = other
        return context
