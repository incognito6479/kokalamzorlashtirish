# Generated by Django 3.1.2 on 2020-11-14 08:48

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('regionroad', '0013_auto_20201112_1046'),
        ('pitomnik', '0035_auto_20201112_0715'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewIrrigation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('changed_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('road_from', models.FloatField()),
                ('road_to', models.FloatField()),
                ('artesian_well', models.PositiveIntegerField()),
                ('drop', models.PositiveIntegerField()),
                ('rain', models.FloatField()),
                ('road', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='regionroad.roaddistrict')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
