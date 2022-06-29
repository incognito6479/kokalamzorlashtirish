# Generated by Django 3.1.2 on 2020-11-12 10:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("regionroad", "0012_auto_20201112_0719"),
    ]

    operations = [
        migrations.AlterField(
            model_name="district",
            name="region",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="districts",
                to="regionroad.region",
            ),
            preserve_default=False,
        ),
    ]
