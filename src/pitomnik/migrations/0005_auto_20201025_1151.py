# Generated by Django 3.1.2 on 2020-10-25 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pitomnik', '0004_auto_20201021_1058'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pitomnikplants',
            name='planted_type',
            field=models.CharField(choices=[('SPROUT', 'Ниҳолдан'), ('SEED', 'Уруғдан')], max_length=10),
        ),
    ]
