import numpy as np
import pytest
from shapely.geometry import Point, Polygon

from map.axes import Axes, Axis
from populate.district import District


def test_intersect():
    axis1 = Axis(Point(0, 0), Point(10, 10), False)
    axis2 = Axis(Point(0, 10), Point(10, 0), False)
    assert axis1.intersect(axis2) == True


def test_intersect2():
    axis1 = Axis(Point(0, 0), Point(0, 0), False)
    axis2 = Axis(Point(10, 10), Point(10, 15), False)
    assert axis1.intersect(axis2) == False


def test_dist_from_point():
    axis1 = Axis(Point(0, 0), Point(10, 10), False)
    point1 = Point(0, 0)
    assert axis1.dist_from_point(point1) == 0


def test_dist_from_point():
    axis1 = Axis(Point(0, 0), Point(0, 0), False)
    point1 = Point(0, 30)
    assert axis1.dist_from_point(point1) == 30


def test_generate_axes_from_district():
    polygon_boundary = Polygon(
        [Point(0, 0), Point(2000, 0), Point(2000, 2000), Point(0, 2000)])
    district = District(1, [1300, 1500])
    axes = Axes()
    district.update_polygon(
        Polygon([Point(10, 16), Point(14, 12), Point(14, 16)]))
    axes.generate_axes_from_district(district, polygon_boundary)
    assert len(axes.axes) > 0


def test_generate_axes_from_district2():
    polygon_boundary = None
    district = District(1, [1300, 1500])
    axes = Axes()
    district.update_polygon(
        Polygon([Point(10, 16), Point(14, 12), Point(14, 16)]))
    axes.generate_axes_from_district(district, polygon_boundary)
    assert len(axes.axes) > 0


@pytest.mark.xfail(
    reason="Nous ne pouvons pas générer d'axes dans un quartier si ce quartier n'a pas de polygone représentant ces limites")
def test_generate_axes_from_district3():
    polygon_boundary = Polygon(
        [Point(0, 0), Point(2000, 0), Point(2000, 2000), Point(0, 2000)])
    district = District(1, [1300, 1500])
    axes = Axes()
    district.update_polygon(None)
    try:
        axes.generate_axes_from_district(district, polygon_boundary)
    except:
        return


@pytest.mark.xfail(reason="Nous ne pouvons pas génèrer des axes dans le quartier si son centre n'y est pas.")
def test_generate_axes_from_district4():
    polygon_boundary = Polygon(
        [Point(0, 0), Point(2000, 0), Point(2000, 2000), Point(0, 2000)])
    district = District(1, [100000, 100000])
    axes = Axes()
    district.update_polygon(
        Polygon([Point(10, 16), Point(14, 12), Point(14, 16)]))
    try:
        axes.generate_axes_from_district(district, polygon_boundary)
    except:
        return


def test_generate_axes_from_voronoi():
    axes = Axes()
    points = [[10, 26], [16, 24], [22, 28]]
    boundary = np.array([[0, 0], [2000, 0], [2000, 2000], [0, 2000]])
    polygons = axes.generate_axes_from_voronoi(boundary, points)
    assert len(polygons) == 3


@pytest.mark.xfail(reason="Il faut au moins 3 points pour créer le polygone des limites de la ville.")
def test_generate_axes_from_voronoi2():
    axes = Axes()
    points = [[10, 26], [16, 24], [22, 28]]
    boundary = np.array([[0, 0], [2000, 0]])
    try:
        polygons = axes.generate_axes_from_voronoi(boundary, points)
    except:
        return


@pytest.mark.xfail(reason="Il faut au moint un point de centre de quartier.")
def test_generate_axes_from_voronoi3():
    axes = Axes()
    points = [[]]
    boundary = np.array([[0, 0], [2000, 0]])
    try:
        polygons = axes.generate_axes_from_voronoi(boundary, points)
    except:
        return


def test_global_goals_aux():
    axes = Axes()
    axis = Axis(Point(0, 0), Point(0, 10), False)
    list = axes.global_goals_aux(axis)
    assert len(list) == 4


def test_global_goals():
    axes = Axes()
    axis = Axis(Point(0, 0), Point(0, 10), False)
    list = axes.global_goals(axis)
    assert len(list) == 2


def test_global_goals2():
    axes = Axes()
    axis = Axis(Point(0, 0), Point(0, 0), False)
    list = axes.global_goals(axis)
    assert len(list) == 2


def test_local_constraints():
    axes = Axes()
    polygon_boundary = Polygon(
        [Point(0, 0), Point(2000, 0), Point(2000, 2000), Point(0, 2000)])
    district = District(1, [500, 500])
    district.update_polygon(polygon_boundary)
    axis = Axis(Point(0, 0), Point(200, 200), False)
    axis2 = Axis(Point(100, 100), Point(800, 300), False)
    axes.axes.append(axis)
    assert axes.local_constraints(axis2, district, polygon_boundary) == False


def test_local_constraints2():
    axes = Axes()
    polygon_boundary = Polygon(
        [Point(0, 0), Point(2000, 0), Point(2000, 2000), Point(0, 2000)])
    district = District(1, [500, 500])
    district.update_polygon(polygon_boundary)
    axis = Axis(Point(0, 0), Point(200, 200), False)
    axis2 = Axis(Point(500, 700), Point(800, 300), False)
    axes.axes.append(axis)
    assert axes.local_constraints(axis2, district, polygon_boundary) == True


@pytest.mark.xfail(reason="Il faut initialiser le quartier.")
def test_local_constraints3():
    axes = Axes()
    polygon_boundary = Polygon(
        [Point(0, 0), Point(2000, 0), Point(2000, 2000), Point(0, 2000)])
    district = None
    axis = Axis(Point(0, 0), Point(200, 200), False)
    axis2 = Axis(Point(500, 700), Point(800, 300), False)
    axes.axes.append(axis)
    try:
        axes.local_constraints(axis2, district, polygon_boundary)
    except:
        return


def test_find_good_point():
    axes = Axes()
    axis = Axis(Point(0, 0), Point(0, 10), False)
    point = Point(0, 5)
    assert isinstance(axes.find_good_point(point, axis), Point)


def test_create_checker_polygon():
    axes = Axes()
    axis = Axis(Point(0, 0), Point(0, 10), False)
    assert isinstance(axes.create_checker_polygon(axis), Polygon)
