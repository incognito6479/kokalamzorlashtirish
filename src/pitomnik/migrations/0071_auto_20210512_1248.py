# Generated by Django 3.1.2 on 2021-05-12 12:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('regionroad', '0015_auto_20201124_1552'),
        ('pitomnik', '0070_merge_20210512_1248'),
    ]

    operations = [
        migrations.AddField(
            model_name='plantedplants',
            name='district',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='regionroad.district'),
        ),
        migrations.AlterField(
            model_name='plantedplants',
            name='metr',
            field=models.IntegerField(null=True),
        ),
    ]
