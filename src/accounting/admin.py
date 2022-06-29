from django.contrib import admin

from accounting.models import DebitCredit, Salary


@admin.register(DebitCredit)
class DebitCreditAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "company",
        "debit",
        "credit",
        "debit_expired",
        "credit_expired",
        "details",
    )


@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "guid",
        "amount",
        "transfer_type",
        "transfer_time",
        "verified",
    )
