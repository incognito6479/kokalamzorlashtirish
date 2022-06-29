from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from django_filters.views import FilterView

from account.models import Organization
from pitomnik.base_mixin import BaseMixin
from pitomnik.filters import IrrigationFilter
from pitomnik.forms import (
    CreateIrrigationForm,
    IrrigationImageFormSet,
    UpdateIrrigationForm,
)
from pitomnik.models import Irrigation, IrrigationImage


class CreateIrrigationView(PermissionRequiredMixin, BaseMixin, CreateView):
    permission_required = [
        "pitomnik.add_irrigation",
    ]
    login_url = "account:login"
    model = Irrigation
    template_name = "pitomnik/irrigation/form.html"
    success_url = reverse_lazy("pitomnik:irrigation:list")
    form_class = CreateIrrigationForm

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["images"] = IrrigationImageFormSet(
                self.request.POST, self.request.FILES
            )
        else:
            data["images"] = IrrigationImageFormSet()
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


class AdminUpdateIrrigationView(PermissionRequiredMixin, UpdateView):
    permission_required = "pitomnik.change_irrigation"
    model = Irrigation
    template_name = "pitomnik/irrigation/form.html"
    success_url = reverse_lazy("pitomnik:irrigation:list_admin")
    form_class = UpdateIrrigationForm

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["images"] = IrrigationImageFormSet(
                self.request.POST, self.request.FILES, instance=self.object
            )
        else:
            data["images"] = IrrigationImageFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        images = context["images"]
        with transaction.atomic():
            # form.instance.added_by = self.request.user
            # form.instance.organization = self.request.user.organization
            self.object = form.save()
            if images.is_valid():
                images.instance = self.object
                images.save()
        return super().form_valid(form)


class UpdateIrrigationView(PermissionRequiredMixin, UpdateView):
    permission_required = "pitomnik.change_irrigation"
    model = Irrigation
    template_name = "pitomnik/irrigation/form.html"
    success_url = reverse_lazy("pitomnik:irrigation:list")
    form_class = UpdateIrrigationForm

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["images"] = IrrigationImageFormSet(
                self.request.POST, self.request.FILES, instance=self.object
            )
        else:
            data["images"] = IrrigationImageFormSet(instance=self.object)
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


class DeleteIrrigationView(PermissionRequiredMixin, DeleteView):
    permission_required = ["pitomnik.delete_irrigation"]
    model = Irrigation
    success_url = reverse_lazy("pitomnik:irrigation:list")


class AdminDeleteIrrigationView(PermissionRequiredMixin, DeleteView):
    permission_required = ["pitomnik.delete_irrigation"]
    model = Irrigation
    success_url = reverse_lazy("pitomnik:irrigation:list_admin")


class IrrigationFilteredListView(PermissionRequiredMixin, FilterView):
    model = Irrigation
    permission_required = [
        "pitomnik.view_irrigation",
    ]
    paginate_by = settings.IRRIGATION_PAGE_SIZE
    template_name = "pitomnik/irrigation/list.html"
    filterset_class = IrrigationFilter

    def get_queryset(self):
        organization = self.request.user.organization
        return Irrigation.objects.get_irrigation_by_organization(organization)


class IrrigationFilteredListViewAdmin(PermissionRequiredMixin, ListView):
    model = Irrigation
    permission_required = [
        "pitomnik.view_irrigation_admin",
    ]
    paginate_by = settings.IRRIGATION_PAGE_SIZE
    template_name = "pitomnik/irrigation/list_admin.html"
    queryset = Irrigation.objects.get_irrigation_list_for_admin()


class IrrigationAdminByOrganization(IrrigationFilteredListView):
    permission_required = "pitomnik.view_irrigation_admin"
    template_name = "pitomnik/irrigation/list_by_organization.html"

    def get_queryset(self):
        organization = get_object_or_404(Organization, pk=self.kwargs["pk"])
        return Irrigation.objects.get_irrigation_by_organization(organization)


class ListIrrigationImages(PermissionRequiredMixin, ListView):
    permission_required = "pitomnik.view_irrigationimage"
    template_name = "pitomnik/irrigation/images.html"

    def get_queryset(self):
        return IrrigationImage.objects.filter_by_irrigation(
            self.kwargs["id"], self.request.user
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context["organization_id"] = get_object_or_404(Irrigation, pk=self.kwargs["id"]).organization_id
        return context
