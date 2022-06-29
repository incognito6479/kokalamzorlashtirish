import csv
import os

from account.models import Organization
from config.settings.base import BASE_DIR
from regionroad.models import District, Region, Road, RoadDistrict

road_type = {
    "Маҳаллий": Road.RoadType.LOCAL,
    "Давлат": Road.RoadType.GOVERNMENT,
    "Халқаро": Road.RoadType.INTERNATIONAL,
}


def insert_region_district():
    fhand = open(
        os.path.join(BASE_DIR, "regionroad/csv_data/region_district.csv"),
        encoding="utf8",
    )
    reader = csv.reader(fhand)
    header = next(reader)
    if header is not None:
        for row in reader:
            region, created = Region.objects.get_or_create(
                name=row[2], code=row[3]
            )
            district, created = District.objects.get_or_create(
                name=row[1], region=region
            )
            district.save()


def insert_road_district():
    fhand = open(
        os.path.join(BASE_DIR, "regionroad/csv_data/full_road.csv"),
        encoding="utf8",
    )
    reader = csv.reader(fhand)
    header = next(reader)
    if header is not None:
        for row in reader:
            print(row)
            try:
                district = District.objects.get(
                    name=row[5],
                )
                road_slice = row[3].split("-")
                road_from = road_slice[0].split(",")[0]
                road_to = road_slice[1]
                if district:
                    road, create = Road.objects.get_or_create(
                        code=row[1],
                        title=row[2],
                        road_type=road_type[row[4]],
                    )
                    road.save()
                    RoadDistrict.objects.get_or_create(
                        road=road,
                        district=district,
                        defaults={
                            "road_from": road_from,
                            "road_to": road_to,
                            "requirement": round(
                                float(road_to) - float(road_from), 2
                            ),
                        },
                    )
            except District.DoesNotExist:
                print(row[5])
                continue


def insert_organization_region():
    fhand = open(
        os.path.join(BASE_DIR, "regionroad/csv_data/tashkilot.csv"),
        encoding="utf8",
    )
    reader = csv.reader(fhand)
    header = next(reader)
    if header is not None:
        for row in reader:
            region = Region.objects.get(name=row[2])
            organization, created = Organization.objects.get_or_create(
                name=row[1], region=region
            )
            organization.save()
    Organization.objects.get_or_create(
        name="УП Ўзйулкукаламзорлаштириш",
        region=Region.objects.get(name="Тошкент шаҳри"),
        status=True,
    )


def run():
    insert_region_district()
    insert_organization_region()
    insert_road_district()
