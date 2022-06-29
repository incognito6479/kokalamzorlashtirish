from django import forms
from django.utils.translation import gettext_lazy as _
from accounting.models import DebitCredit


class DebitCreditForm(forms.ModelForm):
    class Meta:
        model = DebitCredit
        fields = [
            "company",
            "debit",
            "credit",
            "debit_expired",
            "credit_expired",
            "details",
        ]
        labels = {
            'company': _('Корхона ва ташкилотлар номи'),
            'debit': _('Қарздорлик қолдиғи (ДТ)'),
            'credit': _('Қарздорлик қолдиғи (КТ)'),
            'debit_expired': _('Шундан муддати ўтган Қарздорлик қолдиғи (ДТ)'),
            'credit_expired': _('Шундан муддати ўтган Қарздорлик қолдиғи (КТ)'),
            'details': _('Изох'),
        }


# class SalaryForm(forms.ModelForm):
#     class Meta:
#         model = Salary
#         fields = ["amount", "transfer_type", ""]
