# Generated by Django 3.1.2 on 2021-04-25 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pitomnik', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='plantedplants',
            name='metr',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
