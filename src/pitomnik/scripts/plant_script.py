import csv
import os

from config.settings.base import BASE_DIR
from pitomnik.models import Plant

plant_type = {
    "Япроқ баргли дарахт": Plant.PlantType.LEAF_SHAPED,
    "Игна баргли дарахт": Plant.PlantType.CONIFEROUS,
    "Буталар": Plant.PlantType.BUSH,
}


def insert_plants():
    fhand = open(
        os.path.join(BASE_DIR, "pitomnik/csv_data/plant.csv"), encoding="utf-8"
    )
    reader = csv.reader(fhand)
    print(reader)
    header = next(reader)
    if header is not None:
        for row in reader:
            plant, created = Plant.objects.get_or_create(
                type=plant_type[row[2]], name=row[1]
            )
            plant.save()


def run():
    insert_plants()
