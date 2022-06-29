from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from account.models import Organization
from pitomnik.base_mixin import BaseMixin
from pitomnik.forms import (
    CreateLandScapeJobForm,
    LandScapeJobImageFormSet,
    UpdateLandScapeJobForm,
)
from pitomnik.models import LandScapeJob, LandScapeJobImage


class CreateLandScapeJob(PermissionRequiredMixin, BaseMixin, CreateView):
    model = LandScapeJob
    template_name = "pitomnik/landscape_job/form.html"
    form_class = CreateLandScapeJobForm
    success_url = reverse_lazy("pitomnik:landscapejob:list")
    permission_required = [
        "pitomnik.add_landscapejob",
    ]

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["images"] = LandScapeJobImageFormSet(
                self.request.POST, self.request.FILES
            )
        else:
            data["images"] = LandScapeJobImageFormSet()
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


class AdminUpdateLandScapeJob(PermissionRequiredMixin, UpdateView):
    model = LandScapeJob
    template_name = "pitomnik/landscape_job/form.html"
    form_class = UpdateLandScapeJobForm
    success_url = reverse_lazy("pitomnik:landscapejob:list_admin")
    permission_required = [
        "pitomnik.change_landscapejob",
    ]

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["images"] = LandScapeJobImageFormSet(
                self.request.POST, self.request.FILES, instance=self.object
            )
        else:
            data["images"] = LandScapeJobImageFormSet(instance=self.object)
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


class UpdateLandScapeJob(PermissionRequiredMixin, UpdateView):
    model = LandScapeJob
    template_name = "pitomnik/landscape_job/form.html"
    form_class = UpdateLandScapeJobForm
    success_url = reverse_lazy("pitomnik:landscapejob:list")
    permission_required = [
        "pitomnik.change_landscapejob",
    ]

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["images"] = LandScapeJobImageFormSet(
                self.request.POST, self.request.FILES, instance=self.object
            )
        else:
            data["images"] = LandScapeJobImageFormSet(instance=self.object)
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


class DeleteLandScapeJob(PermissionRequiredMixin, DeleteView):
    model = LandScapeJob
    success_url = reverse_lazy("pitomnik:landscapejob:list")
    permission_required = [
        "pitomnik.delete_landscapejob",
    ]


class AdminDeleteLandScapeJob(PermissionRequiredMixin, DeleteView):
    model = LandScapeJob
    success_url = reverse_lazy("pitomnik:landscapejob:list_admin")
    permission_required = [
        "pitomnik.delete_landscapejob",
    ]


class ListLandScapeJob(PermissionRequiredMixin, ListView):
    model = LandScapeJob
    template_name = "pitomnik/landscape_job/list.html"
    permission_required = [
        "pitomnik.view_landscapejob",
    ]
    paginate_by = settings.SAVING_JOB_PAGE_SIZE

    def get_queryset(self):
        return LandScapeJob.objects.filter_by_organization(
            self.request.user.organization
        )


class ListLandScapeJobAdmin(PermissionRequiredMixin, ListView):
    model = LandScapeJob
    template_name = "pitomnik/landscape_job/list_admin.html"
    permission_required = "pitomnik.view_landscapejob_admin"
    queryset = LandScapeJob.objects.aggregate_total()


class ListLandScapeJobByOrganizationAdmin(ListLandScapeJob):
    permission_required = "pitomnik.view_landscapejob_admin"
    template_name = "pitomnik/landscape_job/list_by_organization.html"

    def get_queryset(self):
        organization = get_object_or_404(Organization, pk=self.kwargs["pk"])
        return LandScapeJob.objects.filter_by_organization_admin(organization)


class ListLandScapeJobImages(PermissionRequiredMixin, ListView):
    permission_required = "pitomnik.view_landscapejobimage"
    template_name = "pitomnik/landscape_job/images.html"

    def get_queryset(self):
        return LandScapeJobImage.objects.filter_by_landscapejob(
            self.kwargs["id"], self.request.user
        )
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context["organization_id"] = get_object_or_404(LandScapeJob, pk=self.kwargs["id"]).organization_id
        return context
