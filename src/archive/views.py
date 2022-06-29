from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView

from archive.models import Saving


class ListSaving(PermissionRequiredMixin, ListView):
    model = Saving
    template_name = "archive/saving/list.html"
    paginate_by = 20
    permission_required = [
        "archive.view_saving",
    ]

    def get_queryset(self):
        return Saving.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context["total_quantity"] = Saving.objects.total_quantity()
        return context
