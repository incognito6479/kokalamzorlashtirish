# Generated by Django 3.1.2 on 2020-11-25 21:09

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pitomnik", "0048_plantedplants_planting_side"),
    ]

    operations = [
        migrations.AddField(
            model_name="plantedplants",
            name="planted_date",
            field=models.DateField(default=datetime.date.today),
        ),
    ]
