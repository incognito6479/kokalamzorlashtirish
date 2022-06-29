from django.db import models
from django.db.models import Case, F, Q, Sum, Value, When
from django.utils.translation import gettext_lazy as _

from account.models import Organization, User
from common.models import BaseModel


class DebitCreditQuerySet(models.QuerySet):
    def get_credit_debit_by_organization(self, user):
        return self.filter(organization=user.organization)

    def get_debit_credit_for_admin(self):
        return self.values("organization__name").annotate(
            debit_sum=Sum(F("debit")),
            credit_sum=Sum(F("credit")),
            debit_expired_sum=Sum(F("debit_expired")),
            credit_expired_sum=Sum(F("credit_expired")),
        )


class DebitCreditManager(models.Manager):
    def get_queryset(self):
        return DebitCreditQuerySet(model=self.model, using=self._db)

    def get_credit_debit_by_organization(self, user):
        return self.get_queryset().get_credit_debit_by_organization(user)

    def get_debit_credit_for_admin(self):
        return self.get_queryset().get_debit_credit_for_admin()


class DebitCredit(BaseModel):
    company = models.CharField(max_length=100)
    debit = models.DecimalField(decimal_places=2, max_digits=12)
    credit = models.DecimalField(decimal_places=2, max_digits=12)
    debit_expired = models.DecimalField(decimal_places=2, max_digits=12)
    credit_expired = models.DecimalField(decimal_places=2, max_digits=12)
    details = models.CharField(max_length=100)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    objects = DebitCreditManager()

    def __str__(self):
        return self.details


class SalaryQuerySet(models.QuerySet):
    def get_income_outcome_for_admin(self, date):
        return self.values("organization__name").annotate(
            initial=Sum(
                Case(
                    When(
                        Q(transfer_type=Salary.TransferType.CREDIT)
                        & Q(transfer_time__lt=date),
                        then="amount",
                    ),
                    default=Value("0"),
                )
            )
            - Sum(
                Case(
                    When(
                        Q(transfer_type=Salary.TransferType.DEBIT)
                        & Q(transfer_time__lt=date),
                        then="amount",
                    ),
                    default=Value("0"),
                )
            ),
            income=Sum(
                Case(
                    When(
                        Q(transfer_type=Salary.TransferType.CREDIT)
                        & Q(transfer_time=date),
                        then="amount",
                    ),
                    default=Value("0"),
                )
            ),
            outcome=Sum(
                Case(
                    When(
                        Q(transfer_type=Salary.TransferType.DEBIT)
                        & Q(transfer_time=date),
                        then="amount",
                    ),
                    default=Value("0"),
                )
            ),
        )


class SalaryManager(models.Manager):
    def get_queryset(self):
        return SalaryQuerySet(model=self.model, using=self._db)

    def get_income_outcome_for_admin(self, date=None):
        return self.get_queryset().get_income_outcome_for_admin(date)


class Salary(BaseModel):
    class TransferType(models.TextChoices):
        CREDIT = "CREDIT", _("Кирим")
        DEBIT = "DEBIT", _("Чиқим")

    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    transfer_time = models.DateField(blank=True, null=True)
    transfer_type = models.CharField(
        choices=TransferType.choices, max_length=50
    )
    verified = models.BooleanField(default=False)
    objects = SalaryManager()
