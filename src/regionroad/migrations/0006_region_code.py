# Generated by Django 3.1.2 on 2020-11-10 11:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('regionroad', '0005_roaddistrict_requirement'),
    ]

    operations = [
        migrations.AddField(
            model_name='region',
            name='code',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
