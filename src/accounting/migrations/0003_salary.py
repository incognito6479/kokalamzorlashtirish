# Generated by Django 3.1.2 on 2020-11-04 09:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("account", "0003_auto_20201013_0859"),
        ("accounting", "0002_auto_20201103_1257"),
    ]

    operations = [
        migrations.CreateModel(
            name="Salary",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "guid",
                    models.UUIDField(
                        default=uuid.uuid4, editable=False, unique=True
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(auto_now_add=True, db_index=True),
                ),
                (
                    "changed_at",
                    models.DateTimeField(auto_now=True, db_index=True),
                ),
                (
                    "amount",
                    models.DecimalField(decimal_places=2, max_digits=12),
                ),
                ("transfer_time", models.DateField()),
                (
                    "transfer_type",
                    models.CharField(
                        choices=[("CREDIT", "Кирим"), ("DEBIT", "Чиқим")],
                        max_length=50,
                    ),
                ),
                ("verified", models.BooleanField(default=False)),
                (
                    "added_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "organization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="account.organization",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
