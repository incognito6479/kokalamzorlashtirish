# Generated by Django 3.1.2 on 2020-11-14 10:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("pitomnik", "0037_delete_pitomnikplantitems"),
    ]

    operations = [
        migrations.RenameField(
            model_name="pitomnikplants",
            old_name="creator",
            new_name="added_by",
        ),
    ]