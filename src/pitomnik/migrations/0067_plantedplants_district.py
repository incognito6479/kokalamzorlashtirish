# Generated by Django 3.1.2 on 2021-04-25 10:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('regionroad', '0001_initial'),
        ('pitomnik', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='plantedplants',
            name='district',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='regionroad.district'),
        ),
    ]