# Generated by Django 3.1.2 on 2020-10-14 14:58

from django.db import migrations, models
import vehicles.models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0005_auto_20201014_1457'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='registration_plate',
            field=models.CharField(max_length=10, unique=True, validators=[vehicles.models.validate_registration_plate]),
        ),
    ]
