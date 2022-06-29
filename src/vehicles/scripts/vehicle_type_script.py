import csv
import os

from account.models import User
from config.settings.base import BASE_DIR
from vehicles.models import VehicleTypes


def insert_vehicle_types():
    fhand = open(
        os.path.join(BASE_DIR, "vehicles/csv_data/vehicle.csv"),
        encoding="utf-8",
    )
    reader = csv.reader(fhand)
    print(reader)
    header = next(reader)
    if header is not None:
        for row in reader:
            vehicle, create = VehicleTypes.objects.get_or_create(
                name=row[1],
                added_by=User.objects.filter(is_superuser=True).first(),
            )
            vehicle.save()


def run():
    insert_vehicle_types()
