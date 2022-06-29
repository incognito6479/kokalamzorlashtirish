import re

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Count
from django.utils.translation import gettext_lazy as _

from account.models import Organization, User
from common.models import BaseModel


def validate_registration_plate(val):
    if not re.match("^[0-9]{2}[0-9]{3}[A-Z]{3}$", val):
        raise ValidationError(
            "Давлат рақамин нотоғри кирилтилди (Намуна: 01123ААА)"
        )


OUT = _("Ташқарида")
IN = _("Айвонда")

STORAGE_CHOICES = (
    (OUT, _("Ташқарида")),
    (IN, _("Айвонда")),
)

GOOD = _("Соз")
BAD = _("Носоз")

TECH_STATE_CHOICES = ((GOOD, _("Соз")), (BAD, _("Носоз")))

INSTALLED = _("Ўрнатилган")
NOT_INSTALLED = _("Ўрнатилмаган")

INSTALLED_GPS_STATUS = (
    (INSTALLED, _("Ўрнатилган")),
    (NOT_INSTALLED, _("Ўрнатилмаган")),
)


class VehicleManager(models.Manager):
    def get_vehicle_with_regions(self, user):
        return (
            self.get_queryset()
            .filter(organization=user.organization)
            .order_by("-created_at")
        )

    def get_vehicle_by_organization(self, organization):
        return (
            self.get_queryset()
            .all()
            .filter(organization=organization)
            # .order_by("-created_at")
        )

    def get_count_by_organization(self):
        return (
            self.get_queryset()
            .values("organization__name", "organization__id")
            .annotate(sum=Count("id"))
            .exclude(
                organization__name__in=["Admin", "УП Ўзйулкукаламзорлаштириш"]
            )
            .order_by("organization__id")
        )

    def get_count_by_type_organization(self):
        return (
            self.get_queryset()
            .values("type__name")
            .annotate(sum=Count("id"))
            .values("organization", "sum", "type__name")
            .order_by("type__name")
        )


class VehicleTypes(BaseModel):
    name = models.CharField(max_length=255)
    added_by = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Vehicle(BaseModel):
    objects = VehicleManager()
    type = models.ForeignKey(
        VehicleTypes, on_delete=models.PROTECT, blank=True, null=True
    )
    name = models.CharField(max_length=255, blank=False, null=False)
    manufactured_date = models.DateField(blank=False, null=False)
    registration_plate = models.CharField(
        max_length=10,
        # validators=[validate_registration_plate],
        blank=True,
        null=True,
        unique=True,
    )
    GPS_status = models.CharField(
        choices=INSTALLED_GPS_STATUS,
        max_length=12,
        blank=False,
        null=False,
        default=NOT_INSTALLED,
    )
    storage_site = models.CharField(
        choices=STORAGE_CHOICES,
        max_length=15,
        blank=False,
        null=False,
        default=OUT,
    )
    tech_state = models.CharField(
        choices=TECH_STATE_CHOICES,
        max_length=5,
        default=GOOD,
        blank=True,
        null=True,
    )
    balance_value = models.FloatField(null=True, blank=True)
    aging_value = models.FloatField(null=True, blank=True)
    mileage_value_start_year = models.FloatField(null=True, blank=True)
    mileage_value_report_time = models.FloatField(null=True, blank=True)
    inventory = models.CharField(max_length=255, null=True, blank=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.registration_plate}"
