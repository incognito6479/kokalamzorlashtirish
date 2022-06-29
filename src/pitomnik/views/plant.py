from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView

from django_filters.views import FilterView

from pitomnik.base_mixin import BaseMixin
from pitomnik.filters import PlantFilter
from pitomnik.forms import PlantForm
from pitomnik.models import Plant


class ListPlantView(PermissionRequiredMixin, FilterView):
    permission_required = "pitomnik.view_plant"
    paginate_by = settings.PLANT_PAGE_SIZE
    template_name = "pitomnik/plant/list.html"
    queryset = Plant.objects.all()
    ordering = "-id"
    filterset_class = PlantFilter


class CreatePlantView(PermissionRequiredMixin, BaseMixin, CreateView):
    permission_required = "pitomnik.add_plant"
    model = Plant
    template_name = "pitomnik/plant/add.html"
    success_url = reverse_lazy("pitomnik:plant:list")
    form_class = PlantForm


class UpdatePlantView(PermissionRequiredMixin, UpdateView):
    permission_required = "pitomnik.change_plant"
    model = Plant
    template_name = "pitomnik/plant/add.html"
    success_url = reverse_lazy("pitomnik:plant:list")
    form_class = PlantForm


class DeletePlantView(PermissionRequiredMixin, DeleteView):
    permission_required = "pitomnik.delete_plant"
    model = Plant
    success_url = reverse_lazy("pitomnik:plant:list")
    template_name = "pitomnik/plant_type-pitomnik_list.html"
