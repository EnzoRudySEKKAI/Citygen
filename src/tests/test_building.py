from math import *

from shapely.geometry import Point, Polygon

from map.axes import Axis
from populate.building import Building


def test_create_building():
    axis = Axis(Point(395, 225), Point(412, 234), False)
    building = Building(axis, 2, Building.HOUSE)
    created_building = building.create_building(axis, 2)

    assert isinstance(created_building, Polygon)

    polygon_ = building.create_building(axis, 1)
    assert isinstance(polygon_.area, float)


def test_random_point_on_a_segment():
    axis = Axis(Point(395, 225), Point(412, 234), False)
    building = Building(axis, 2, Building.HOUSE)

    random_point = building.random_point_on_a_segment(480, 500, 285, 290)
    assert isinstance(random_point, Point)


def test_get_angle_between_points():
    axis = Axis(Point(395, 225), Point(412, 234), False)
    building = Building(axis, 2, Building.HOUSE)

    angle = building.get_angle_between_points(0, 0, 1, 1)
    assert angle == radians(45)

    angle = building.get_angle_between_points(0, 0, 0, 0)
    assert angle == radians(0.0)
