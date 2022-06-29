# Generated by Django 3.1.2 on 2020-12-18 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vehicles", "0010_auto_20201212_1614"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="vehicle",
            name="inspection",
        ),
        migrations.RemoveField(
            model_name="vehicle",
            name="oil_change",
        ),
        migrations.AddField(
            model_name="vehicle",
            name="inventory",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]