# Generated by Django 3.1.2 on 2020-12-23 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vehicles", "0013_vehicletypes_added_by"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vehicle",
            name="GPS_status",
            field=models.CharField(
                choices=[
                    ("Ўрнатилган", "Ўрнатилган"),
                    ("Ўрнатилмаган", "Ўрнатилмаган"),
                ],
                default="Ўрнатилмаган",
                max_length=12,
            ),
        ),
    ]
