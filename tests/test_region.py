import pytest

from account.models import Organization, User
from pitomnik.models import Plant, PlantedPlants
from regionroad.models import District, Region, Road, RoadDistrict


@pytest.fixture
def simple_data():
    region = Region.objects.create(
        name="Tashkent", coordinates="{}", code=1111
    )

    organization = Organization.objects.create(
        name="organization", region=region
    )
    user = User.objects.create(
        phone_number="+998946545999", organization=organization
    )
    mahalliy = RoadType.objects.create(type_name="mahalliy")
    RoadType.objects.create(type_name="davlat")
    RoadType.objects.create(type_name="xalqaro")
    m34 = Road.objects.create(title="m34", road_type=mahalliy)
    leaf = PlantType.objects.create(name="leaf", added_by=user)
    nail = PlantType.objects.create(name="nail", added_by=user)
    bush = PlantType.objects.create(name="bush", added_by=user)
    plant_leaf = Plant.objects.create(name="plant_name", plant_type=leaf)
    Plant.objects.create(name="plant_name2", plant_type=nail)
    Plant.objects.create(name="plant_name3", plant_type=bush)
    district = District.objects.create(name="Yunusobod")
    road_district = RoadDistrict.objects.create(
        road=m34, district=district, road_from=1, road_to=100, requirement=100
    )
    PlantedPlants.objects.create(
        plant=plant_leaf,
        road_from=1,
        road_to=11,
        added_by=user,
        quantity=1,
        road_district=road_district,
    )


@pytest.mark.django_db
def test_check_aggregation(simple_data):
    # Given
    name = "Tashkent"
    expected_result = [
        {
            "region_name": "Tashkent",
            "total_quantity": 10,
            "leaf_quantity": 2,
            "bushed_quantity": 3,
            "nail_quantity": 5,
            "road_slice": 10,
            "road_type": [
                {
                    "type_name": "mahalliy",
                    "total_quantity": 5,
                    "leaf_quantity": 1,
                    "bushed_quantity": 2,
                    "nail_quantity": 2,
                    "road_slice": 5,
                },
                {
                    "type_name": "davlat",
                    "total_quantity": 0,
                    "leaf_quantity": 0,
                    "bushed_quantity": 0,
                    "nail_quantity": 0,
                    "road_slice": 5,
                },
                {
                    "type_name": "xalqaro",
                    "total_quantity": 0,
                    "leaf_quantity": 0,
                    "bushed_quantity": 0,
                    "nail_quantity": 0,
                    "road_slice": 0,
                },
            ],
        }
    ]

    # When
    result = Region.objects.get_planted_plant_statistics()
    # Then
    assert result == expected_result
