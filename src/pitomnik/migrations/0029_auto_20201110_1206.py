# Generated by Django 3.1.2 on 2020-11-10 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pitomnik", "0028_auto_20201109_1023"),
    ]

    operations = [
        migrations.AddField(
            model_name="plantedplants",
            name="road_from",
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="plantedplants",
            name="road_to",
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
    ]
