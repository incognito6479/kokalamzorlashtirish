# Generated by Django 3.1.2 on 2020-11-14 12:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pitomnik', '0040_merge_20201114_1712'),
    ]

    operations = [
        migrations.RenameField(
            model_name='newirrigation',
            old_name='road',
            new_name='road_district',
        ),
    ]
