import csv
import os

from account.models import User
from config.settings.base import BASE_DIR
from pitomnik.models import Pitomnik, PitomnikPlants, Plant

pitomnik_list = [
    'УП "Каракалпакйулкукалам"',
    'УП "Aндижанйулкукалам"',
    'УП "Бухарайулкукалам"',
    'УП "Джизакйулкукалам"',
    'УП "Кашкадарьяйулкукалам"',
    'УП "Навоийулкукалам"',
    'УП "Намангайулкукалам"',
    'УП "Самаркандйулкукалам"',
    'УП "Сырдарьяйулкукалам"',
    'УП "Сурхандарьяйулкукалам"',
    'УП "Ташкентйулкукалам"',
    'УП "Ферганайулкукалам"',
    'УП "Хорезмйулкукалам"',
]


def insert_pitomnik_plants():
    fhand = open(
        os.path.join(BASE_DIR, "pitomnik/csv_data/pitomnik_plant.csv"),
        encoding="utf-8",
    )
    reader = csv.reader(fhand)
    print(reader)
    header = next(reader)
    if header is not None:
        for row in reader:
            plant = Plant.objects.get(name=row[2])
            for i in range(13):
                quantity = float(row[i + 3])
                if quantity > 0:
                    pitomnik = Pitomnik.objects.get(
                        name=pitomnik_list[i] + " ПИТОМНИК"
                    )
                    pitomnik_plants, _ = PitomnikPlants.objects.get_or_create(
                        pitomnik=pitomnik,
                        plant=plant,
                        quantity=quantity,
                        plant_type=PitomnikPlants.PlantType.SPROUT,
                        plant_field=0,
                        planted_date="2020-09-01",
                        readiness_date="2020-09-01",
                        added_by=User.objects.get(pk=1),
                    )
                    pitomnik_plants.save()


def run():
    insert_pitomnik_plants()
