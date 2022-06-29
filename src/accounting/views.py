from datetime import datetime

from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from pitomnik.base_mixin import BaseMixin

from .forms import DebitCreditForm
from .models import DebitCredit, Salary


class CreateDebitCredit(PermissionRequiredMixin, BaseMixin, CreateView):
    model = DebitCredit
    template_name = "accounting/debitcredit/add.html"
    form_class = DebitCreditForm
    success_url = reverse_lazy("accounting:debitcredit:list")
    permission_required = [
        "accounting.add_debitcredit",
    ]


class UpdateDebitCredit(PermissionRequiredMixin, UpdateView):
    model = DebitCredit
    template_name = "accounting/debitcredit/change.html"
    form_class = DebitCreditForm
    success_url = reverse_lazy("accounting:debitcredit:list")
    permission_required = [
        "accounting.change_debitcredit",
    ]


class DeleteDebitCredit(PermissionRequiredMixin, DeleteView):
    model = DebitCredit
    template_name = "accounting/debitcredit/change.html"
    success_url = reverse_lazy("accounting:debitcredit:list")
    permission_required = [
        "accounting.delete_debitcredit",
    ]


class ListDebitCredit(PermissionRequiredMixin, ListView):
    model = DebitCredit
    template_name = "accounting/debitcredit/list.html"
    permission_required = [
        "accounting.view_debitcredit",
    ]
    paginate_by = settings.DEBIT_CREDIT_PAGE_SIZE

    def get_queryset(self):
        return DebitCredit.objects.all()


class ListDebitCreditAdmin(PermissionRequiredMixin, ListView):
    model = DebitCredit
    template_name = "accounting/debitcredit/admin_list.html"
    permission_required = ["accounting.view_debitcredit_admin"]
    paginate_by = settings.DEBIT_CREDIT_PAGE_SIZE

    def get_queryset(self):
        return DebitCredit.objects.get_debit_credit_for_admin()


class ListSalaryView(PermissionRequiredMixin, ListView):
    model = Salary
    template_name = "accounting/salary/admin_list.html"
    permission_required = ["accounting.view_salary__admin"]
    paginate_by = 20

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context["date"] = self.request.GET.get("date", datetime.today().date())
        return context

    def get_queryset(self):
        return Salary.objects.get_income_outcome_for_admin(
            self.request.GET.get("date", datetime.today().date())
        )


class CreateSalaryView(PermissionRequiredMixin, CreateView):
    model = Salary
    template_name = "accounting/salary/add.html"
    permission_required = ["accounting.add_salary"]
