import pytest

from city import City
from populate.district import DISTRICTS_TYPE


def test_get_axes_list():
    city = City(4, 800, 800, 20, DISTRICTS_TYPE)
    city.create_major_axes()
    assert len(city.get_axes_list()) > 0


def test_get_buildings():
    city = City(4, 800, 800, 20, DISTRICTS_TYPE)
    city.create_major_axes()
    for district in city.districts:
        city.create_district_axes(district)
        city.populate(district)
    assert not len(city.get_buildings()) <= 10
    assert not len(city.get_buildings()) > 20
    assert len(city.get_buildings()) <= 20


def test_create_major_axes():
    city = City(4, 800, 800, 20, DISTRICTS_TYPE)
    city.create_major_axes()
    assert len(city.major_axes.axes) > 0


def test_populate():
    city = City(4, 800, 800, 20, DISTRICTS_TYPE)
    city.create_major_axes()
    for district in city.districts:
        city.create_district_axes(district)
        city.populate(district)
    for district in city.districts:
        assert len(district.buildings) > 0


@pytest.mark.xfail(reason="On ne génère pas de ville sans quartier.")
def test_city_with_no_districts():
    city = City(0, 800, 800, 0, DISTRICTS_TYPE)
    try:
        city.create_major_axes()
    except IndexError:
        return
        
@pytest.mark.xfail(reason="On ne génère pas de ville avec 1 quartier.")
def test_city_with_one_districts():
    city = City(1, 800, 800, 0, DISTRICTS_TYPE)
    try:
        city.create_major_axes()
    except IndexError:
        return

@pytest.mark.xfail(reason="On ne génère pas de ville de taille 0 en hateur ou en longueur.")
def test_city_with_0_width():
    city = City(5, 0, 800, 20, DISTRICTS_TYPE)
    try:
        city.create_major_axes()
    except:
        return
