from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.views.generic.base import View

from django_filters.views import FilterView

from account.models import Organization
from pitomnik.base_mixin import BaseMixin
from pitomnik.filters import SavingJobFilter
from pitomnik.forms import (
    CreateSavingJobForm,
    SavingJobImageFormSet,
    UpdateSavingJobForm,
)
from pitomnik.models import SavingJob, SavingjobImage
from utils.download_file import download


class CreateSavingJobView(PermissionRequiredMixin, BaseMixin, CreateView):
    permission_required = "pitomnik.add_savingjob"
    model = SavingJob
    template_name = "pitomnik/saving_job/form.html"
    success_url = reverse_lazy("pitomnik:savingjob:list")
    form_class = CreateSavingJobForm

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["images"] = SavingJobImageFormSet(
                self.request.POST, self.request.FILES
            )
        else:
            data["images"] = SavingJobImageFormSet()
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


class UpdateAdminSavingJobView(PermissionRequiredMixin, UpdateView):
    permission_required = "pitomnik.change_savingjob"
    model = SavingJob
    template_name = "pitomnik/saving_job/form.html"
    success_url = reverse_lazy("pitomnik:savingjob:list_admin")
    form_class = UpdateSavingJobForm

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["images"] = SavingJobImageFormSet(
                self.request.POST, self.request.FILES, instance=self.object
            )
        else:
            data["images"] = SavingJobImageFormSet(instance=self.object)
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        images = context["images"]
        with transaction.atomic():
            self.object = form.save()
            if images.is_valid():
                images.instance = self.object
                images.save()
        return super().form_valid(form)


class UpdateSavingJobView(PermissionRequiredMixin, UpdateView):
    permission_required = "pitomnik.change_savingjob"
    model = SavingJob
    template_name = "pitomnik/saving_job/form.html"
    success_url = reverse_lazy("pitomnik:savingjob:list")
    form_class = UpdateSavingJobForm

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["images"] = SavingJobImageFormSet(
                self.request.POST, self.request.FILES, instance=self.object
            )
        else:
            data["images"] = SavingJobImageFormSet(instance=self.object)
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


class DeleteSavingJobView(PermissionRequiredMixin, DeleteView):
    permission_required = "pitomnik.delete_savingjob"
    model = SavingJob
    success_url = reverse_lazy("pitomnik:savingjob:list")


class AdminDeleteSavingJobView(PermissionRequiredMixin, DeleteView):
    permission_required = "pitomnik.delete_savingjob"
    model = SavingJob
    success_url = reverse_lazy("pitomnik:savingjob:list_admin")


class ListSavingJobView(PermissionRequiredMixin, FilterView):
    permission_required = "pitomnik.view_savingjob"
    paginate_by = settings.SAVING_JOB_PAGE_SIZE
    template_name = "pitomnik/saving_job/list.html"
    filterset_class = SavingJobFilter

    def get_queryset(self):
        return SavingJob.objects.filter_by_organization(self.request.user)


class ListSavingJobAdminView(PermissionRequiredMixin, FilterView):
    permission_required = "pitomnik.view_savingjob_admin"
    paginate_by = settings.SAVING_JOB_PAGE_SIZE
    template_name = "pitomnik/saving_job/list_admin.html"
    queryset = SavingJob.objects.aggregate_quantity_len()
    filterset_class = SavingJobFilter


class ListSavingJobByOrganizationAdmin(ListSavingJobView):
    permission_required = "pitomnik.view_savingjob_admin"
    template_name = "pitomnik/saving_job/list_by_organization.html"

    def get_queryset(self):
        organization = get_object_or_404(Organization, pk=self.kwargs["pk"])
        return SavingJob.objects.filter_by_organization_admin(organization)


class DownloadSavingJobView(View):
    def get(self, request, *args, **kwargs):
        organization = Organization.objects.get(pk=self.kwargs["pk"])
        saving_job = SavingJob.objects.filter_by_organization_admin(
            organization
        )
        saving_job = saving_job.values_list(
            "road_district__road__title",
            "road_from",
            "road_to",
            "tree_quantity",
            "tree_len",
            "dig_quantity",
            "dig_len",
            "organic_quantity",
            "organic_len",
            "workers_quantity",
            "technique_quantity",
        )
        data = list(saving_job)
        path = "saving_job"
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


class ListSavingJobImages(PermissionRequiredMixin, ListView):
    permission_required = "pitomnik.view_savingjobimage"
    template_name = "pitomnik/saving_job/images.html"

    def get_queryset(self):
        return SavingjobImage.objects.filter_by_savingjob(
            self.kwargs["id"], self.request.user
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context["organization_id"] = get_object_or_404(
            SavingJob, pk=self.kwargs["id"]
        ).organization_id
        return context
