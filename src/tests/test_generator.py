import numpy as np
from scipy.spatial import Voronoi

from map import generator


def test_voronoi():
    districts_voronoi = generator.voronoi(4, 800, 800)
    assert isinstance(districts_voronoi, Voronoi)


def test_voronoi_polygons():
    districts_voronoi = generator.voronoi(4, 800, 800)
    voronoi_polygons = generator.voronoi_polygons(districts_voronoi, np.linalg.norm(1))
    assert isinstance(voronoi_polygons, list)
