from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db import transaction
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from account.models import Organization
from pitomnik.forms import PitomnikForm, PitomnikImageFormSet
from pitomnik.models import Pitomnik, PitomnikImage


class CreatePitomnikView(PermissionRequiredMixin, CreateView):
    model = Pitomnik
    template_name = "pitomnik/pitomnik_add.html"
    form_class = PitomnikForm
    success_url = reverse_lazy("pitomnik:pitomnik:list")
    permission_required = "pitomnik.add_pitomnik"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["images"] = PitomnikImageFormSet(
                self.request.POST, self.request.FILES
            )
        else:
            data["images"] = PitomnikImageFormSet()
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


class UpdatePitomnikView(PermissionRequiredMixin, UpdateView):
    model = Pitomnik
    template_name = "pitomnik/pitomnik_add.html"
    form_class = PitomnikForm
    success_url = reverse_lazy("pitomnik:pitomnik:list")
    permission_required = "pitomnik.change_pitomnik"

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data["images"] = PitomnikImageFormSet(
                self.request.POST, self.request.FILES, instance=self.object
            )
        else:
            data["images"] = PitomnikImageFormSet(instance=self.object)
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


class ListPitomnikView(PermissionRequiredMixin, ListView):
    permission_required = "pitomnik.view_pitomnik"
    paginate_by = settings.PITOMNIK_PAGE_SIZE
    template_name = "pitomnik/pitomnik_list.html"
    context_object_name = "pitomniks"

    def get_queryset(self):
        if self.request.user.is_staff:
            return Pitomnik.objects.all()
        else:
            return Pitomnik.objects.filter(organization_id=int(self.request.user.organization_id))


class AdminListPitomnikView(ListPitomnikView):
    permission_required = "pitomnik.view_pitomnik_admin"
    template_name = "pitomnik/pitomnik_admin_list.html"

    def get_queryset(self):
        organization = get_object_or_404(Organization, pk=self.kwargs["id"])
        return Pitomnik.objects.filter_by_organization(organization)


class ListPitomnikImages(PermissionRequiredMixin, ListView):
    permission_required = "pitomnik.view_pitomnikimage"
    template_name = "pitomnik/images.html"

    def get_queryset(self):
        return PitomnikImage.objects.filter_by_pitomnik(
            self.kwargs["id"], self.request.user
        )


class DeletePitomnikView(PermissionRequiredMixin, DeleteView):
    permission_required = ["pitomnik.delete_pitomnik"]
    model = Pitomnik
    success_url = reverse_lazy("pitomnik:pitomnik:list")
