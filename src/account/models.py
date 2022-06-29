from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from phonenumber_field.modelfields import PhoneNumberField

from common.models import BaseModel
from regionroad.models import Region


class OrganizationQuerySet(models.QuerySet):
    def get_organizations(self):
        return (
            self.values("name", "id", "region__name")
            .exclude(name__in=["Admin", "УП Ўзйулкукаламзорлаштириш"])
            .order_by("id")
        )


class OrganizationManager(models.Manager):
    def get_queryset(self):
        return OrganizationQuerySet(self.model, using=self._db)

    def get_organizations(self):
        return self.get_queryset().get_organizations()


class Organization(BaseModel):
    objects = OrganizationManager()
    name = models.CharField(max_length=255, null=False, blank=False)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True)
    status = models.BooleanField(default=False)

    class Meta:
        verbose_name = _("Organization")
        verbose_name_plural = _("Organizations")

    def __str__(self):
        return f"{self.name}"


class UserManager(BaseUserManager):
    def get_all_users_by_organization(self, user):
        exclude_options = ["Маҳаллий админ", "Бош Aдмин"]
        return (
            self.get_queryset()
            .filter(
                organization=user.organization,
                is_superuser=False,
                is_staff=False,
            )
            .exclude(groups__name__in=exclude_options)
            .order_by("-id")
        )

    def _create_user(
        self, phone_number, password, organization, **extra_fields
    ):
        if not phone_number:
            raise ValueError("The given phone number must be set")
        if not organization:
            raise ValueError("Organization must be set")

        user = self.model(
            phone_number=phone_number,
            organization=organization,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self, phone_number, password=None, organization=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", False)
        return self._create_user(
            phone_number, password, organization, **extra_fields
        )

    def create_superuser(self, phone_number, password, **extra_fields):
        organization, is_new = Organization.objects.get_or_create(name="Admin")
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        user = self.create_user(
            phone_number, password, organization, **extra_fields
        )
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    phone_number = PhoneNumberField(
        _("Phone number"),
        unique=True,
        help_text=_("Required. Only international format used."),
        error_messages={
            "unique": _("User with this phone number already exists.")
        },
        blank=False,
        null=False,
    )
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    email = models.EmailField(_("email address"), blank=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_(
            "Designates whether the user can log into this admin site."
        ),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting account."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "phone_number"

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.phone_number}"
