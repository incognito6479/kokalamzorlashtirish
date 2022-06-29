from django.urls import include, path

from .views import (
    CreateDebitCredit,
    DeleteDebitCredit,
    ListDebitCredit,
    ListDebitCreditAdmin,
    ListSalaryView,
    UpdateDebitCredit,
)

app_name = "accounting"

debitcredit_urls = [
    path("", ListDebitCredit.as_view(), name="list"),
    path("add/", CreateDebitCredit.as_view(), name="add"),
    path("<int:pk>/change/", UpdateDebitCredit.as_view(), name="change"),
    path("<int:pk>/delete/", DeleteDebitCredit.as_view(), name="delete"),
    path("admin-list/", ListDebitCreditAdmin.as_view(), name="admin_list"),
]

salary_urls = [path("", ListSalaryView.as_view(), name="list")]

urlpatterns = [
    path("debitcredit/", include((debitcredit_urls, "debitcredit"))),
    path("salary/", include((salary_urls, "salary"))),
]
