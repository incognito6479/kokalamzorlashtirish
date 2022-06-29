from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from pitomnik.base_mixin import BaseMixin
from pitomnik.forms import PitomnikSavingJobForm, PitomnikSavingJobImageFormSet
from pitomnik.models import PitomnikSavingJob, PitomnikSavingJobImage


class CreatePitomnikSavingJob(PermissionRequiredMixin, BaseMixin, CreateView):
    permission_required = "pitomnik.add_pitomniksavingjob"
    model = PitomnikSavingJob
    template_name = "pitomnik/pitomnik_saving_job/add.html"
    success_url = reverse_lazy("pitomnik:pitomniksavingjob:list")
    form_class = PitomnikSavingJobForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["images"] = PitomnikSavingJobImageFormSet(
                self.request.POST, self.request.FILES
            )
        else:
            data["images"] = PitomnikSavingJobImageFormSet()
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


class UpdatePitomnikSavingJob(PermissionRequiredMixin, UpdateView):
    permission_required = "pitomnik.change_pitomniksavingjob"
    model = PitomnikSavingJob
    template_name = "pitomnik/pitomnik_saving_job/add.html"
    success_url = reverse_lazy("pitomnik:pitomniksavingjob:list")
    form_class = PitomnikSavingJobForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["images"] = PitomnikSavingJobImageFormSet(
                self.request.POST, self.request.FILES, instance=self.object
            )
        else:
            data["images"] = PitomnikSavingJobImageFormSet(
                instance=self.object
            )
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


class DeletePitomnikSavingJob(PermissionRequiredMixin, DeleteView):
    permission_required = "pitomnik.delete_pitomniksavingjob"
    model = PitomnikSavingJob
    success_url = reverse_lazy("pitomnik:pitomniksavingjob:list")


class ListPitomnikSavingJob(PermissionRequiredMixin, ListView):
    model = PitomnikSavingJob
    permission_required = ["pitomnik.view_pitomniksavingjob"]
    template_name = "pitomnik/pitomnik_saving_job/list.html"
    paginate_by = settings.PITOMNIK_SAVING_JOB_PAGE_SIZE

    def get_queryset(self):
        return PitomnikSavingJob.objects.get_saving_job_by_organization(
            self.request.user.organization
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context[
            "plant_type_object"
        ] = PitomnikSavingJob.objects.group_by_plant_type(
            self.request.user.organization
        )
        return context


class ListPitomnikSavingJobImages(PermissionRequiredMixin, ListView):
    permission_required = "pitomnik.view_pitomniksavingjobimage"
    template_name = "pitomnik/pitomnik_saving_job/images.html"

    def get_queryset(self):
        return PitomnikSavingJobImage.objects.filter_by_pitomniksavingjob(
            self.kwargs["id"], self.request.user
        )
