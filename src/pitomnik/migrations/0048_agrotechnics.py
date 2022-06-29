# Generated by Django 3.1.2 on 2020-11-25 11:36

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('pitomnik', '0047_pitomnikplants_planted_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Agrotechnics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('guid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('changed_at', models.DateTimeField(auto_now=True, db_index=True)),
                ('total_plants', models.IntegerField(default=0)),
                ('planted_area', models.FloatField(default=0)),
                ('agrotechnical_measures', models.FloatField(default=0)),
                ('mineral', models.FloatField(default=0)),
                ('organic', models.FloatField(default=0)),
                ('workers', models.IntegerField(default=0)),
                ('technique', models.IntegerField(default=0)),
                ('plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pitomnik.plant')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
