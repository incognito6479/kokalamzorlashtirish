import csv
import os

from account.models import Organization, User
from config.settings.base import BASE_DIR
from pitomnik.models import Pitomnik
from regionroad.models import Region


def insert_pitomnik_organization():
    fhand = open(
        os.path.join(BASE_DIR, "pitomnik/csv_data/pitomnik.csv"),
        encoding="utf-8",
    )
    reader = csv.reader(fhand)
    print(reader)
    header = next(reader)
    if header is not None:
        for row in reader:
            region = Region.objects.get(name=row[2])
            region.save()
            organization = Organization.objects.get(name=row[1])
            organization.save()
            user = User.objects.filter(is_superuser=True).first()
            pitomnik, created = Pitomnik.objects.get_or_create(
                name=row[1] + " ПИТОМНИК",
                address=row[2],
                kontr=0,
                area=0,
                organization=organization,
                added_by=user,
            )
            pitomnik.save()


def run():
    insert_pitomnik_organization()
