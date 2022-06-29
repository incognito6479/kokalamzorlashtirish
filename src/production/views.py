from decimal import DivisionUndefined

from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.views.generic.base import View

from django_filters.views import FilterView

from account.models import Organization
from regionroad.models import Road
from utils.download_file import download

from .filters import (
    IrrigationProductionFilter,
    LandscapeProductionFilter,
    MonthlyProductionFilter,
    PlantingProductionFilter,
    SavingProductionFilter,
    YearlyProductionFilter,
)
from .forms import (
    IrrigationProductionForm,
    LandscapeProductionForm,
    MonthlyProductionPlanForm,
    PlantingProductionForm,
    SavingProductionForm,
    StatForm,
    StatRepublicForm,
    YearlyProductionPlanForm,
)
from .models import (
    BaseModelProduction,
    IrrigationProduction,
    LandscapeJobProduction,
    MonthlyProductionPlan,
    PlantingProduction,
    SavingJobProduction,
    YearlyProductionPlan,
)


class CreateIrrigationProduction(CreateView, PermissionRequiredMixin):
    permission_required = "production.add_irrigationproduction"
    model = IrrigationProduction
    template_name = "production/create_irrigation.html"
    success_url = reverse_lazy("production:irrigation:list")
    form_class = IrrigationProductionForm

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        form.instance.organization = self.request.user.organization
        form.instance.production_type = (
            BaseModelProduction.ProductionType.IRRIGATION
        )
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class CreateSavingJobProduction(CreateView, PermissionRequiredMixin):
    permission_required = "production.add_savingjobproduction"
    model = SavingJobProduction
    template_name = "production/create_savingjob.html"
    success_url = reverse_lazy("production:saving:list")
    form_class = SavingProductionForm

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        form.instance.organization = self.request.user.organization
        form.instance.production_type = (
            BaseModelProduction.ProductionType.SAVING
        )
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class CreatePlantingProduction(CreateView, PermissionRequiredMixin):
    permission_required = "production.add_plantingproduction"
    model = PlantingProduction
    template_name = "production/create_planting.html"
    success_url = reverse_lazy("production:planting:list")
    form_class = PlantingProductionForm

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        form.instance.organization = self.request.user.organization
        form.instance.production_type = (
            BaseModelProduction.ProductionType.PLANTING
        )
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class CreateLandscapeJobProduction(CreateView, PermissionRequiredMixin):
    permission_required = "production.add_landscapejobproduction"
    model = PlantingProduction
    template_name = "production/create_landscape.html"
    success_url = reverse_lazy("production:landscape:list")
    form_class = LandscapeProductionForm

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        form.instance.organization = self.request.user.organization
        form.instance.production_type = (
            BaseModelProduction.ProductionType.LANDSCAPE
        )
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class IrrigationProductionListView(PermissionRequiredMixin, FilterView):
    permission_required = "production.view_irrigationproduction"
    template_name = "production/list_irrigation.html"
    paginate_by = settings.DISTRICT_ROAD_PAGE_SIZE
    filterset_class = IrrigationProductionFilter

    def get_queryset(self):
        return IrrigationProduction.objects.get_by_organization(
            self.request.user
        )


class SavingProductionListView(PermissionRequiredMixin, FilterView):
    permission_required = "production.view_savingjobproduction"
    template_name = "production/list_saving.html"
    paginate_by = settings.DISTRICT_ROAD_PAGE_SIZE
    filterset_class = SavingProductionFilter

    def get_queryset(self):
        return SavingJobProduction.objects.get_by_organization(
            self.request.user
        )


class PlantingProductionListView(PermissionRequiredMixin, FilterView):
    permission_required = "production.view_plantingproduction"
    template_name = "production/list_planting.html"
    paginate_by = settings.DISTRICT_ROAD_PAGE_SIZE
    filterset_class = PlantingProductionFilter

    def get_queryset(self):
        return PlantingProduction.objects.get_by_organization(
            self.request.user
        )


class LandscapeJobProductionListView(PermissionRequiredMixin, FilterView):
    permission_required = "production.view_landscapejobproduction"
    template_name = "production/list_landscape.html"
    paginate_by = settings.DISTRICT_ROAD_PAGE_SIZE
    filterset_class = LandscapeProductionFilter

    def get_queryset(self):
        return LandscapeJobProduction.objects.get_by_organization(
            self.request.user
        )


class ListMonthlyProdPlanAJAX(PermissionRequiredMixin, ListView):
    template_name = "production/monthly_plan_by_year.html"
    permission_required = "production.view_monthlyproductionplan"

    def get_queryset(self):
        year = self.request.GET.get("year")
        month = self.request.GET.get("month")
        return MonthlyProductionPlan.objects.get_by_year_and_organization(
            user=self.request.user, year=year, month=month
        )


class ListYearLyProdPlanAJAX(PermissionRequiredMixin, ListView):
    template_name = "production/monthly_plan_by_year.html"
    permission_required = "production.view_yearlyproductionplan"

    def get_queryset(self):
        year = self.request.GET.get("year")
        organization = self.request.GET.get("organization")
        organization = Organization.objects.get(pk=organization)
        return YearlyProductionPlan.objects.get_by_year_and_organization(
            year=year, organization=organization
        )


class CreateYearlyProdView(PermissionRequiredMixin, CreateView):
    permission_required = "production.add_yearlyproductionplan"
    template_name = "production/create_yearlyprodplan.html"
    form_class = YearlyProductionPlanForm
    success_url = reverse_lazy("production:yearly:list")

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        return super().form_valid(form)


class CreateMonthlyProdView(PermissionRequiredMixin, CreateView):
    permission_required = "production.add_monthlyproductionplan"
    template_name = "production/create_monthly_plan.html"
    form_class = MonthlyProductionPlanForm
    success_url = reverse_lazy("production:monthly:list")


class ListMonthProdView(PermissionRequiredMixin, FilterView):
    permission_required = "production.view_monthlyproductionplan"
    template_name = "production/list_monthlyprodplan.html"
    paginate_by = settings.DISTRICT_ROAD_PAGE_SIZE
    queryset = MonthlyProductionPlan.objects.get_list()
    filterset_class = MonthlyProductionFilter


class ListYearlyProdView(PermissionRequiredMixin, FilterView):
    permission_required = "production.view_yearlyproductionplan"
    template_name = "production/list_yearlyprodplan.html"
    paginate_by = settings.DISTRICT_ROAD_PAGE_SIZE
    queryset = YearlyProductionPlan.objects.get_all()
    filterset_class = YearlyProductionFilter
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ListYearlyProdView, self).get_context_data()
        context['user_org_id'] = int(self.request.user.organization_id)
        return context

class StatByOrganizationAndYear(PermissionRequiredMixin, ListView):
    permission_required = "production.view_yearlyproductionplan"
    template_name = "production/stats_by_organization.html"
    paginate_by = settings.DISTRICT_ROAD_PAGE_SIZE

    def get_queryset(self):
        form = StatForm(data=self.request.GET)
        if form.is_valid() and int(form.data["organization"]) == self.request.user.organization_id:
            return YearlyProductionPlan.objects.get_by_year_month_organization(
                form.data["year"],
                form.data["month"],
                form.data["organization"],
            )
        return YearlyProductionPlan.objects.none()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()

        data = {
            "year": self.request.GET.get("year", 2020),
            "month": self.request.GET.get("month", 1),
            "organization": self.request.GET.get("organization", 2),
        }
        context['user_org'] = str(self.request.user.organization)
        context["form"] = StatForm(data=data)
        context["year"] = self.request.GET.get("year")
        context["month"] = self.request.GET.get("month")
        context["organization"] = self.request.GET.get("organization")
        context[
            "sum"
        ] = YearlyProductionPlan.objects.get_by_year_month_organization_sum(
            year=data["year"],
            month=data["month"],
            organization=data["organization"],
        )
        return context


class StatByOrganizationAndYearRoadType(PermissionRequiredMixin, ListView):
    permission_required = "production.view_yearlyproductionplan"
    template_name = "production/stat_by_republic.html"
    paginate_by = settings.DISTRICT_ROAD_PAGE_SIZE

    def get_queryset(self):
        form = StatRepublicForm(data=self.request.GET)
        if form.is_valid():
            return Road.objects.get_pto_republic_stat(
                year=form.data["year"],
                month=form.data["month"],
            )
        return Road.objects.none()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        data = {
            "year": self.request.GET.get("year", 2020),
            "month": self.request.GET.get("month", 1),
        }
        context['user_org_id'] = int(self.request.user.organization_id)
        context["form"] = StatRepublicForm(data=data)
        context["year"] = self.request.GET.get("year")
        context["month"] = self.request.GET.get("month")
        context["organizations"] = Organization.objects.get_organizations()
        # context["republic"] = Road.objects.get_pto_republic_stat_sum(
        #     year=data["year"], month=data["month"]
        # )
        # context["republic_total"] = Road.objects.get_pto_republic_stat_total(
        #     year=data["year"], month=data["month"]
        # )
        return context


class DownloadProductionView(View):
    def percent(self, number=None, number_op=None):
        try:
            return round(((int(number) / int(number_op)) * 100), 2)
        except DivisionUndefined and TypeError and ZeroDivisionError:
            return 0

    def append_to_list(self, query):
        list_data = [
            query.get("yearly_plan_money"),
            query.get("monthly_plan_sum_until_month"),
            query.get("production_money_until_month"),
            self.percent(
                query.get("production_money_until_month"),
                query.get("monthly_plan_sum_until_month"),
            ),
            query.get("monthly_financing_sum_until_month"),
            query.get("monthly_plan_sum_month"),
            query.get("production_money_month"),
            self.percent(
                query.get("production_money_month"),
                query.get("monthly_plan_sum_month"),
            ),
            query.get("monthly_financing_sum_month"),
        ]
        return list_data

    def get(self, request, *args, **kwargs):
        form = StatRepublicForm(data=self.request.GET)
        if form.is_valid():
            query = Road.objects.get_pto_republic_stat(
                year=form.data["year"],
                month=form.data["month"],
            )
            republic = Road.objects.get_pto_republic_stat_sum(
                year=form.data["year"],
                month=form.data["month"],
            )
        else:
            query = Road.objects.none()
            republic = Road.objects.none()
        data = []
        exclude_organizations = ["Admin", "УП Ўзйулкукаламзорлаштириш"]
        organization_list = Organization.objects.exclude(name__in=exclude_organizations)
        for organization in organization_list:
            data.append(([""] * 9))
            xalqaro = [""] * 9
            davlat = [""] * 9
            maxalliy = [""] * 9
            for row in query:
                if row.get("yearly__organization") == organization.id:
                    if row.get("road_type") == 1:
                        xalqaro = self.append_to_list(row)
                    if row.get("road_type") == 2:
                        davlat = self.append_to_list(row)
                    if row.get("road_type") == 3:
                        maxalliy = self.append_to_list(row)
            data.append(xalqaro)
            data.append(davlat)
            data.append(maxalliy)

        data.append(([""] * 9))
        for row in list(republic):
            data.append(self.append_to_list(row))
        path = "pto"
        row_start_index = 5
        column_start_index = 3
        column_end_range = 11
        indexing = False
        return download(
            data,
            path,
            row_start_index,
            column_start_index,
            column_end_range,
            indexing,
        )


class UpdateIrrigationProduction(PermissionRequiredMixin, UpdateView):
    permission_required = "production.change_irrigationproduction"
    template_name = "production/create_irrigation.html"
    form_class = IrrigationProductionForm
    success_url = reverse_lazy("production:irrigation:list")
    model = IrrigationProduction

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        form.instance.organization = self.request.user.organization
        form.instance.production_type = (
            BaseModelProduction.ProductionType.IRRIGATION
        )
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class UpdateSavingJobProduction(PermissionRequiredMixin, UpdateView):
    permission_required = "production.change_savingjobproduction"
    template_name = "production/create_savingjob.html"
    form_class = SavingProductionForm
    success_url = reverse_lazy("production:saving:list")
    model = SavingJobProduction

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        form.instance.organization = self.request.user.organization
        form.instance.production_type = (
            BaseModelProduction.ProductionType.SAVING
        )
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class UpdatePlantingProduction(PermissionRequiredMixin, UpdateView):
    permission_required = "production.change_plantingproduction"
    template_name = "production/create_planting.html"
    form_class = PlantingProductionForm
    success_url = reverse_lazy("production:planting:list")
    model = PlantingProduction

    def form_valid(self, form):
        form.instance.added_by = self.request.user
        form.instance.organization = self.request.user.organization
        form.instance.production_type = (
            BaseModelProduction.ProductionType.PLANTING
        )
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs


class UpdateLandScapeJobProduction(PermissionRequiredMixin, UpdateView):
    permission_required = "production.change_landscapejobproduction"
    template_name = "production/create_landscape.html"
    form_class = LandscapeProductionForm
    success_url = reverse_lazy("production:landscape:list")
    model = LandscapeJobProduction


class UpdateYearlyProdView(PermissionRequiredMixin, UpdateView):
    permission_required = "production.change_yearlyproductionplan"
    template_name = "production/create_yearlyprodplan.html"
    form_class = YearlyProductionPlanForm
    success_url = reverse_lazy("production:yearly:list")
    model = YearlyProductionPlan


class UpdateMonthlyProdView(PermissionRequiredMixin, UpdateView):
    permission_required = "production.change_monthlyproductionplan"
    template_name = "production/create_monthly_plan.html"
    form_class = MonthlyProductionPlanForm
    success_url = reverse_lazy("production:monthly:list")
    model = MonthlyProductionPlan


class DeleteIrrigationView(PermissionRequiredMixin, DeleteView):
    permission_required = "production.delete_irrigationproduction"
    model = IrrigationProduction
    success_url = reverse_lazy("production:irrigation:list")


class DeleteLandScapeJobProductionView(PermissionRequiredMixin, DeleteView):
    permission_required = "production.delete_landscapejobproduction"
    model = LandscapeJobProduction
    success_url = reverse_lazy("production:landscape:list")


class DeletePlantingProductionView(PermissionRequiredMixin, DeleteView):
    permission_required = "production.delete_plantingproduction"
    model = PlantingProduction
    success_url = reverse_lazy("production:planting:list")


class DeleteSavingJobProductionView(PermissionRequiredMixin, DeleteView):
    permission_required = "production.delete_savingjobproduction"
    model = SavingJobProduction
    success_url = reverse_lazy("production:saving:list")


class DeleteMonthlyProdView(PermissionRequiredMixin, DeleteView):
    permission_required = "production.delete_monthlyproductionplan"
    model = MonthlyProductionPlan
    success_url = reverse_lazy("production:monthly:list")


class DeleteYearlyProdView(PermissionRequiredMixin, DeleteView):
    permission_required = "production.delete_yearlyproductionplan"
    model = YearlyProductionPlan
    success_url = reverse_lazy("production:yearly:list")
