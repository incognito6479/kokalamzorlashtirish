# Generated by Django 3.1.2 on 2020-10-13 05:51

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("regionroad", "__first__"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Pitomnik",
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
                ("name", models.CharField(max_length=255)),
                ("address", models.TextField()),
                ("area", models.FloatField()),
                (
                    "added_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "district",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="regionroad.district",
                    ),
                ),
                (
                    "organization",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="regionroad.organization",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="PitomnikPlants",
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
                ("quantity", models.PositiveIntegerField()),
                (
                    "planted_type",
                    models.CharField(
                        choices=[("SPROUT", "SPROUT"), ("SEED", "SEED")],
                        max_length=10,
                    ),
                ),
                ("area", models.FloatField()),
                ("expected_ready_time", models.DateField()),
                (
                    "added_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "pitomnik",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="pitomnik.pitomnik",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Pitomnik Plants",
            },
        ),
        migrations.CreateModel(
            name="PlantType",
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
                ("name", models.CharField(max_length=255)),
                (
                    "added_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="PlantedPlants",
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
                ("quantity", models.PositiveIntegerField()),
                (
                    "road_slice",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.FloatField(), size=None
                    ),
                ),
                ("location", models.JSONField()),
                (
                    "added_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "pitomnik_plant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="pitomnik.pitomnikplants",
                    ),
                ),
                (
                    "road",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="regionroad.road",
                    ),
                ),
            ],
            options={
                "verbose_name": "Planted Plant",
                "verbose_name_plural": "Planted Plants",
            },
        ),
        migrations.CreateModel(
            name="Plant",
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
                ("name", models.CharField(max_length=255)),
                (
                    "added_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "plant_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="plants",
                        to="pitomnik.planttype",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.AddField(
            model_name="pitomnikplants",
            name="plant",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="pitomnik.plant",
            ),
        ),
        migrations.AddField(
            model_name="pitomnik",
            name="plants",
            field=models.ManyToManyField(
                related_name="pitomnik",
                through="pitomnik.PitomnikPlants",
                to="pitomnik.Plant",
            ),
        ),
    ]
