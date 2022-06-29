from regionroad.models import RoadDistrict, Road


def run():
    for r in RoadDistrict.objects.filter(
            road__road_type=Road.RoadType.INTERNATIONAL):
        r.road_to = r.road_to
        r.save()

    for r in RoadDistrict.objects.filter(
            road__road_type=Road.RoadType.GOVERNMENT):
        r.road_to = r.road_to
        r.save()

    for r in RoadDistrict.objects.filter(road__road_type=Road.RoadType.LOCAL):
        r.road_to = r.road_to
        r.save()
