# Generated by Django 3.1.2 on 2020-10-13 08:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20201013_0814'),
        ('pitomnik', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pitomnik',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.organization'),
        ),
    ]
