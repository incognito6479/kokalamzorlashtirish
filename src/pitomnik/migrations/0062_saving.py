# Generated by Django 3.1.2 on 2020-12-21 12:27

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("pitomnik", "0061_auto_20201218_1354"),
    ]

    operations = [
        migrations.CreateModel(
            name="Saving",
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
                ("name", models.CharField(max_length=100)),
                ("tree_quantity", models.PositiveIntegerField()),
            ],
            options={
                "abstract": False,
            },
        ),
    ]