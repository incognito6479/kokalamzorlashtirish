# Generated by Django 3.1.2 on 2020-10-29 15:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("pitomnik", "0016_irrigation_irrigationtype_landscapejob_savingjob"),
    ]

    operations = [
        migrations.AddField(
            model_name="irrigation",
            name="irrigation_type",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                to="pitomnik.irrigationtype",
            ),
            preserve_default=False,
        ),
    ]
