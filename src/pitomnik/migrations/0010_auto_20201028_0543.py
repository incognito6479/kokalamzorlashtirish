# Generated by Django 3.1.2 on 2020-10-28 05:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("pitomnik", "0009_plantedplantimage"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="plantedplants",
            name="pitomnik",
        ),
        migrations.RemoveField(
            model_name="plantedplants",
            name="plant",
        ),
        migrations.AddField(
            model_name="plantedplants",
            name="pitomnik_plant",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="pitomnik.pitomnikplants",
            ),
            preserve_default=False,
        ),
    ]