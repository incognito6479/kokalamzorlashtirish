import csv
import os

from archive.models import Saving
from config.settings.base import BASE_DIR


def insert_saving():
    fhand = open(
        os.path.join(BASE_DIR, "archive/csv_data/saving.csv"), encoding="utf-8"
    )
    reader = csv.reader(fhand)
    print(reader)
    header = next(reader)
    if header is not None:
        for row in reader:
            saving, created = Saving.objects.get_or_create(
                name=row[0],
                tree_quantity=row[1],
            )
            saving.save()


def run():
    insert_saving()
