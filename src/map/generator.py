import random as rd
from collections import defaultdict

import numpy as np
from scipy.spatial import Voronoi
from shapely.geometry import Polygon


def voronoi(nb_districts, width, height):
    """
    Cette fonction va créer un tableau d'objet Voronoi représentant les quartiers de la ville.

    Args:
        nb_districts (int): Le nombre de quartier de la ville.
        width (int): Largeur de la ville.
        height (int): Longueur de la ville.

    Returns:
        [Voronoi]: Une liste d'objet Voronoi.
    """
    # initialisation du tableau de point
    array = np.zeros([nb_districts, 2], np.int32)

    for i in range(nb_districts):  # choisir un point aléatoire pour chaques quartiers
        array[i][0] = np.uint16(rd.randint(0, width))
        array[i][1] = np.uint16(rd.randint(0, height))

    voronoi_ = Voronoi(array)

    return voronoi_


def voronoi_polygons(voronoi_, diameter):
    """
    Cette fonction a été développé par Gareth Rees elle a été trouvée sur StackOverflow.
    https://stackoverflow.com/questions/23901943/voronoi-compute-exact-boundaries-of-every-region
    Tout le code sur stackoverflow est sous la license Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)
    et est donc utilisable.

    Generate shapely.geometry.Polygon objects corresponding to the
    regions of a scipy.spatial.Voronoi object, in the order of the
    input points. The polygons for the infinite regions are large
    enough that all points within a distance 'diameter' of a Voronoi
    vertex are contained in one of the infinite polygons.
    """
    result = []
    centroid = voronoi_.points.mean(axis=0)

    # Mapping from (input point index, Voronoi point index) to list of
    # unit vectors in the directions of the infinite ridges starting
    # at the Voronoi point and neighbouring the input point.
    ridge_direction = defaultdict(list)
    for (p, q), rv in zip(voronoi_.ridge_points, voronoi_.ridge_vertices):
        u, v = sorted(rv)
        if u == -1:
            # Infinite ridge starting at ridge point with index v,
            # equidistant from input points with indexes p and q.
            t = voronoi_.points[q] - voronoi_.points[p]  # tangent
            n = np.array([-t[1], t[0]]) / np.linalg.norm(t)  # normal
            midpoint = voronoi_.points[[p, q]].mean(axis=0)
            direction = np.sign(np.dot(midpoint - centroid, n)) * n
            ridge_direction[p, v].append(direction)
            ridge_direction[q, v].append(direction)

    for i, r in enumerate(voronoi_.point_region):
        region = voronoi_.regions[r]
        if -1 not in region:
            # Finite region.
            # yield Polygon(voronoi.vertices[region])
            result.append(Polygon(voronoi_.vertices[region]))
            continue
        # Infinite region.
        inf = region.index(-1)  # Index of vertex at infinity.
        j = region[(inf - 1) % len(region)]  # Index of previous vertex.
        k = region[(inf + 1) % len(region)]  # Index of next vertex.
        if j == k:
            # Region has one Voronoi vertex with two ridges.
            dir_j, dir_k = ridge_direction[i, j]
        else:
            # Region has two Voronoi vertices, each with one ridge.
            dir_j, = ridge_direction[i, j]
            dir_k, = ridge_direction[i, k]

        # Length of ridges needed for the extra edge to lie at least
        # 'diameter' away from all Voronoi vertices.
        length = 2 * diameter / np.linalg.norm(dir_j + dir_k)

        # Polygon consists of finite part plus an extra edge.
        finite_part = voronoi_.vertices[region[inf + 1:] + region[:inf]]
        extra_edge = [voronoi_.vertices[j] + dir_j * length,
                      voronoi_.vertices[k] + dir_k * length]
        # yield Polygon(np.concatenate((finite_part, extra_edge)))
        result.append(Polygon(np.concatenate((finite_part, extra_edge))))
    return result
