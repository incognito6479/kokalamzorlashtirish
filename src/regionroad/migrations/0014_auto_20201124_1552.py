# Generated by Django 3.1.2 on 2020-11-24 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("regionroad", "0013_auto_20201112_1046"),
    ]

    operations = [
        migrations.AlterField(
            model_name="road",
            name="road_type",
            field=models.IntegerField(
                choices=[(3, "Маҳаллий"), (2, "Давлат"), (1, "Халқаро")]
            ),
        ),
        migrations.AlterUniqueTogether(
            name="roaddistrict",
            unique_together={("road", "district")},
        ),
    ]