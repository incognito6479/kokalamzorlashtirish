# Generated by Django 3.1.2 on 2020-12-14 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pitomnik', '0055_auto_20201213_1606'),
    ]

    operations = [
        migrations.AddField(
            model_name='pitomnikplants',
            name='dried',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
