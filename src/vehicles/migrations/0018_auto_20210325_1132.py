# Generated by Django 3.1.2 on 2021-03-25 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0017_merge_20210325_1132'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='registration_plate',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True),
        ),
    ]