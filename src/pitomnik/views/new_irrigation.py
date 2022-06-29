from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from django_filters.views import FilterView

from account.models import Organization
from pitomnik.base_mixin import BaseMixin
from pitomnik.filters import NewIrrigationFilter
from pitomnik.forms import (
    CreateNewIrrigationForm,
    NewIrrigationImageFormSet,
    UpdateNewIrrigationForm,
)
from pitomnik.models import NewIrrigation, NewIrrigationImage


class CreateNewIrrigationView(PermissionRequiredMixin, BaseMixin, CreateView):
    permission_required = ["pitomnik.add_newirrigation"]
    model = NewIrrigation
    template_name = "pitomnik/new_irrigation/form.html"
    success_url = reverse_lazy("pitomnik:newirrigation:list")
    form_class = CreateNewIrrigationForm

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["images"] = NewIrrigationImageFormSet(
                self.request.POST, self.request.FILES
            )
        else:
            data["images"] = NewIrrigationImageFormSet()
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


class ListNewIrrigationView(PermissionRequiredMixin, FilterView):
    model = NewIrrigation
    permission_required = ["pitomnik.view_newirrigation"]
    template_name = "pitomnik/new_irrigation/list.html"
    paginate_by = settings.NEW_IRRIGATION_PAGE_SIZE
    filterset_class = NewIrrigationFilter

    def get_queryset(self):
        return NewIrrigation.objects.filter_by_organization(
            self.request.user.organization
        )


class AdminUpdateNewIrrigationView(PermissionRequiredMixin, UpdateView):
    model = NewIrrigation
    template_name = "pitomnik/new_irrigation/form.html"
    form_class = UpdateNewIrrigationForm
    success_url = reverse_lazy("pitomnik:newirrigation:list_admin")
    permission_required = ["pitomnik.change_newirrigation"]

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["images"] = NewIrrigationImageFormSet(
                self.request.POST, self.request.FILES, instance=self.object
            )
        else:
            data["images"] = NewIrrigationImageFormSet(instance=self.object)
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


class UpdateNewIrrigationView(PermissionRequiredMixin, UpdateView):
    model = NewIrrigation
    template_name = "pitomnik/new_irrigation/form.html"
    form_class = UpdateNewIrrigationForm
    success_url = reverse_lazy("pitomnik:newirrigation:list")
    permission_required = ["pitomnik.change_newirrigation"]

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["images"] = NewIrrigationImageFormSet(
                self.request.POST, self.request.FILES, instance=self.object
            )
        else:
            data["images"] = NewIrrigationImageFormSet(instance=self.object)
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


class DeleteNewIrrigationView(PermissionRequiredMixin, DeleteView):
    permission_required = ["pitomnik.delete_newirrigation"]
    model = NewIrrigation
    success_url = reverse_lazy("pitomnik:newirrigation:list")


class AdminDeleteNewIrrigationView(PermissionRequiredMixin, DeleteView):
    permission_required = ["pitomnik.delete_newirrigation"]
    model = NewIrrigation
    success_url = reverse_lazy("pitomnik:newirrigation:list_admin")


class ListNewIrrigationAdminView(PermissionRequiredMixin, ListView):
    permission_required = "pitomnik.view_newirrigation_admin"
    paginate_by = settings.NEW_IRRIGATION_PAGE_SIZE
    template_name = "pitomnik/new_irrigation/list_admin.html"
    queryset = NewIrrigation.objects.aggregate_sum()


class ListNewIrrigationByOrganizationAdmin(ListNewIrrigationView):
    permission_required = "pitomnik.view_newirrigation_admin"
    template_name = "pitomnik/new_irrigation/list_by_organization.html"

    def get_queryset(self):
        organization = get_object_or_404(Organization, pk=self.kwargs["pk"])
        return NewIrrigation.objects.filter_by_organization(organization)


class ListNewIrrigationImages(PermissionRequiredMixin, ListView):
    permission_required = "pitomnik.view_newirrigationimage"
    template_name = "pitomnik/new_irrigation/images.html"

    def get_queryset(self):
        return NewIrrigationImage.objects.filter_by_newirrigation(
            self.kwargs["id"], self.request.user
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context["organization_id"] = get_object_or_404(
            NewIrrigation, pk=self.kwargs["id"]
        ).organization_id
        return context
