import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from account.models import Organization

from .models import (
    IrrigationProduction,
    LandscapeJobProduction,
    MonthlyProductionPlan,
    PlantingProduction,
    SavingJobProduction,
    YearlyProductionPlan,
)

MONTHS = (
    (1, "Январь"),
    (2, "Февраль"),
    (3, "Март"),
    (4, "Апрель"),
    (5, "Май"),
    (6, "Июнь"),
    (7, "Июль"),
    (8, "Август"),
    (9, "Сентабрь"),
    (10, "Октябрь"),
    (11, "Ноябрь"),
    (12, "Декабрь"),
)

exclude_options = ["Admin", "УП Ўзйулкукаламзорлаштириш"]


def year_choices():
    return [(r, r) for r in range(2010, datetime.date.today().year + 3)]


def set_month_prod(self):
    monthly_id = None
    if "monthly_prod_plan" in self.data:
        try:
            monthly_id = int(self.data.get("monthly_prod_plan"))
        except (ValueError, TypeError):
            pass
    elif self.instance.pk:
        monthly_id = self.instance.monthly_prod_plan.id
    if monthly_id:
        try:
            self.fields[
                "monthly_prod_plan"
            ].queryset = MonthlyProductionPlan.objects.filter(id=monthly_id)
        except IntegrityError:
            pass


class BaseForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        years = list(
            set(YearlyProductionPlan.objects.get_years_by_organization(user))
        )
        year_choices = [(years[i][0], years[i][0]) for i in range(len(years))]
        if user is not None:
            self.fields["year"].choices = year_choices
        self._set_monthly_prod()
        self._set_label()

    year = forms.ChoiceField(label="Йил")
    monthly_prod_plan = forms.ModelChoiceField(
        queryset=MonthlyProductionPlan.objects.none(),
        label="Ойлик режа",
    )
    months = forms.ChoiceField(choices=MONTHS, label="Ой")

    def _set_monthly_prod(self):
        set_month_prod(self)

    def _set_label(self):
        self.fields["quantity"].label = "Сони"
        self.fields["money_amount"].label = "Суммаси"
        self.fields["LSH"].label = "ЛСҲ"
        self.fields["road_address"].label = "Манзили"


class IrrigationProductionForm(BaseForm):
    class Meta:
        model = IrrigationProduction
        fields = [
            "year",
            "months",
            "monthly_prod_plan",
            "quantity",
            "money_amount",
            "LSH",
            "road_address",
        ]


class SavingProductionForm(BaseForm):
    class Meta:
        model = SavingJobProduction
        fields = [
            "year",
            "months",
            "monthly_prod_plan",
            "quantity",
            "money_amount",
            "LSH",
            "road_address",
        ]


class LandscapeProductionForm(BaseForm):
    error_messages = {
        "invalid_road_address": {
            "road_address": "Йўл манзили тоғри киритинг (Намуна 10)",
        },
    }

    def clean(self):
        if "road_address" in self.data:
            if len(self.data.get("road_address").split(",")) > 1:
                raise ValidationError(
                    self.error_messages["invalid_road_address"],
                    code="invalid_road_address",
                )

    class Meta:
        model = LandscapeJobProduction
        fields = [
            "year",
            "months",
            "monthly_prod_plan",
            "quantity",
            "money_amount",
            "LSH",
            "road_address",
        ]


class PlantingProductionForm(BaseForm):
    class Meta:
        model = PlantingProduction
        fields = [
            "year",
            "months",
            "monthly_prod_plan",
            "quantity",
            "money_amount",
            "LSH",
            "road_address",
        ]


class YearlyProductionPlanForm(forms.ModelForm):
    error_messages = {
        "unique_constraint": "Бундай маълумот базада бор.",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_year()
        self._set_label()

    organization = forms.ModelChoiceField(
        queryset=Organization.objects.exclude(name__in=exclude_options),
        label="Ташкилот номи",
    )
    year_choice = forms.ChoiceField(choices=year_choices(), label="Йил")

    class Meta:
        model = YearlyProductionPlan
        fields = [
            "road",
            "organization",
            "money_amount_plan",
            "road_address",
            "year_choice",
        ]

    def clean(self):
        if (
            ("road" in self.data)
            and ("organization" in self.data)
            and ("road_address" in self.data)
            and ("year_choice" in self.data)
        ):
            print(self.data["year_choice"])
            date = datetime.date(
                year=int(self.data.get("year_choice")),
                month=1,
                day=1,
            )
            yearly = YearlyProductionPlan.objects.filter(
                organization=int(self.data.get("organization")),
                road_address=self.data.get("road_address").split(","),
                road=self.data.get("road"),
                year=date,
            ).exclude(pk=self.instance.id)
            if yearly:
                raise ValidationError(
                    self.error_messages["unique_constraint"],
                    code="unique_constraint",
                )

    def _set_year(self):
        if "year_choice" in self.data:
            self.instance.year = datetime.date(
                year=int(self.data.get("year_choice")), month=1, day=1
            )

    def _set_label(self):
        self.fields["road_address"].label = "Манзили"
        self.fields["road"].label = "Автомобиль йўлининг номи"
        self.fields["money_amount_plan"].label = "Йиллик режа"


class MonthlyProductionPlanForm(forms.ModelForm):
    error_messages = {
        "unique_constraint": "Бундай маълумот базада бор.",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        years = list(set(YearlyProductionPlan.objects.get_years()))
        years_choices = [(years[i][0], years[i][0]) for i in range(len(years))]
        organizations = list(
            Organization.objects.values_list("id", "name").exclude(
                name__in=exclude_options
            )
        )
        organizations_choices = [
            (organizations[i][0], organizations[i][1])
            for i in range(len(organizations))
        ]
        self.fields["years_choices"].choices = years_choices
        self.fields["organizations_choices"].choices = organizations_choices
        self._set_month_year()
        self._set_yearly_prod_plan()
        self._set_label()

    years_choices = forms.ChoiceField(label="Йил")
    organizations_choices = forms.ChoiceField(label="Ташкилот номи")
    yearly_prod_plan = forms.ModelChoiceField(
        queryset=YearlyProductionPlan.objects.none(),
        label="Йиллик режа",
    )
    months_choices = forms.ChoiceField(
        choices=MONTHS,
        label="Ой",
    )

    def clean(self):
        if (
            ("years_choices" in self.data)
            and ("yearly_prod_plan" in self.data)
            and ("months_choices" in self.data)
        ):
            date = datetime.date(
                year=int(self.data.get("years_choices")),
                month=int(self.data.get("months_choices")),
                day=1,
            )
            monthly = MonthlyProductionPlan.objects.filter(
                yearly_prod_plan=int(self.data.get("yearly_prod_plan")),
                month=date,
            ).exclude(pk=self.instance.id)
            if monthly:
                raise ValidationError(
                    self.error_messages["unique_constraint"],
                    code="unique_constraint",
                )

    class Meta:

        model = MonthlyProductionPlan
        fields = [
            "years_choices",
            "organizations_choices",
            "yearly_prod_plan",
            "months_choices",
            "monthly_plan_money",
            "financing",
        ]

    def _set_label(self):
        self.fields["financing"].label = "Молиялаштириш"
        self.fields["monthly_plan_money"].label = "Режа"

    def _set_month_year(self):
        if ("years_choices" in self.data) and ("months_choices" in self.data):
            self.instance.month = datetime.date(
                year=int(self.data.get("years_choices")),
                month=int(self.data.get("months_choices")),
                day=1,
            )
        elif self.instance.pk:
            self.fields["years_choices"].initial = self.instance.month.year
            self.fields["months_choices"].initial = self.instance.month.month

    def _set_yearly_prod_plan(self):
        yearly_id = None
        if "yearly_prod_plan" in self.data:
            try:
                yearly_id = int(self.data.get("yearly_prod_plan"))
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields[
                "organizations_choices"
            ].initial = self.instance.yearly_prod_plan.organization.id
            yearly_id = self.instance.yearly_prod_plan.id

        if yearly_id:
            self.fields[
                "yearly_prod_plan"
            ].queryset = YearlyProductionPlan.objects.filter(id=yearly_id)
            self.fields["yearly_prod_plan"].initial = yearly_id


class StatForm(forms.Form):
    year = forms.ChoiceField(choices=year_choices(), label="Йил", initial=2000)
    month = forms.ChoiceField(choices=MONTHS, label="Ой", initial=1)
    organization = forms.ModelChoiceField(
        queryset=Organization.objects.exclude(name__in=exclude_options),
        label="Ташкилот номи",
        initial=2,
    )


class StatRepublicForm(forms.Form):
    year = forms.ChoiceField(choices=year_choices(), label="Йил", initial=2000)
    month = forms.ChoiceField(choices=MONTHS, label="Ой", initial=1)
