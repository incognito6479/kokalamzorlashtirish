# Generated by Django 3.1.2 on 2020-11-10 12:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("regionroad", "0006_auto_20201110_1245"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="roaddistrict",
            name="road_slice",
        ),
    ]
