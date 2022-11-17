import random
from math import *

import numpy as np
from scipy.spatial import Voronoi
from shapely.geometry import Polygon, Point, LineString

from map.generator import voronoi_polygons


class Axis:
    """
    Une classe nous permettant de représenter un segment.

    Avec sa position de départ, sa position de fin, et une information sur est-ce que c'est un axe majeur ou non
    """

    def __init__(self, start_pos, end_pos, is_major_axis):
        """Constructeur de l'object Axis.

        Args:
            start_pos (Point): Point de départ de l'axe.
            end_pos (Point): Point d'arrivée de l'axe.
            is_major_axis (bool): Un boolean qui nous dit si l'axe est majeur ou non. 
        """
        self.start_pos = start_pos
        self.end_pos = end_pos
        self.is_major_axis = is_major_axis
        self.size = start_pos.distance(end_pos)

    def intersect(self, axis2):
        """Une fonction permettant de vérifier si un point possède une intersection avec un axe.

        Args:
            axis2 (Axis): Un axe quelconque.

        Returns:
            boolean: Vrai si le point possède une intersection avec l'axe. Faux sinon.
        """
        line = LineString([self.start_pos, self.end_pos])
        line2 = LineString([axis2.start_pos, axis2.end_pos])
        return line.intersects(line2)

    def dist_from_point(self, point):
        """Cette fonction renvoie la distance entre le point actuel et le point placé en paramètre.

        Args:
            point (Point): Un Point quelconque.

        Returns:
            int: La distance séparant les deux points.
        """
        return point.distance(LineString([self.end_pos, self.start_pos]))


class Axes:
    """Une classe nous permettant de manipuler une liste d'axes"""

    def __init__(self):
        """Crée une objet Axes qui contient une liste d'axes vide.
        """
        self.axes = []

    def generate_axes_from_district(self, district, polygon_boundary):
        """
        Cette fonction prend en pramètre un quartier et un polygon représentant les bords de la ville.
        Elle va ensuite générer les axes mineurs en utilisant global_goals() et local_constraints.
        GlobalGoals propose des axes et local_constraints
        vérifie si les axes proposés sont valides.

        Args:
            district (District): Le quartier dans lequel nous allons générer les axes.
            polygon_boundary (Polygon): Le polygone qui représente les bords de la ville.
        """
        district_center = district.get_district_center_as_point()
        new_point = Point(district_center.x + 20, district_center.y)
        f = Axis(district_center, new_point, False)
        self.axes.append(f)
        q = self.global_goals_aux(f)
        while q:
            axis = q.pop(0)
            if self.local_constraints(axis, district, polygon_boundary):
                self.axes.append(axis)
                axes = self.global_goals(axis)
                for axis2 in axes:
                    q.append(axis2)

    def generate_axes_from_voronoi(self, boundary, points):
        """
        Cette fonction va générer les axes majeurs de la ville. Elle utilise Voronoi.
        Elle va ajouter les axes majeurs à la liste d'axes de l'objet courant. 
        Et ensuite renvoyer un polygon correspondant à ces axes majeurs afin que le quartier puisse connaitre ses limites.

        Args:
            boundary (Polygon): Le polygone représentant les limites de la ville.
            points ([Point]): Les centres des quartiers de la ville.

        Returns:
            [Polygon]: Une liste de polygon.
        """
        diameter = np.linalg.norm(boundary.ptp(axis=0))
        boundary_polygon = Polygon(boundary)
        axes_voronoi = []
        polygons = voronoi_polygons(Voronoi(points), diameter)
        for p in polygons:
            x, y = zip(*p.intersection(boundary_polygon).exterior.coords)
            for i in range(len(x)):
                pos1 = Point(x[i], y[i])
                pos2 = Point(x[(i + 1) % len(x)], y[(i + 1) % len(x)])
                axis = Axis(pos1, pos2, True)
                axes_voronoi.append(axis)

        self.axes.extend(axes_voronoi)
        return polygons

    @staticmethod
    def angle_trunc(a):
        while a < 0.0:
            a += pi * 2
        return a

    def get_angle_between_points(self, x_orig, y_orig, x_end, y_end):
        """
        Renvoie l'angle entre deux points par rapport à l'axe des abscisses.

        Args:
            x_orig (int): Coordonnées du premier point sur l'axe des abscisses.
            y_orig (int): Coordonnées du premier point sur l'axe des ordonnées.
            x_end (int): Coordonnées du deuxième point sur l'axe des abscisses.
            y_end (int): Coordonnées du deuxième point sur l'axe des ordonnées.

        Returns:
            float: L'angle en radians.
        """
        delta_y = y_end - y_orig
        delta_x = x_end - x_orig
        return self.angle_trunc(atan2(delta_y, delta_x))

    def global_goals_aux(self, axis):
        """
        Cette fonction va générer les 4 axes suivants le premier au début de la création des axes mineurs.
        Le premier axe crée 4 axes dans 4 direction différentes.

        Args:
            axis (Axis): Le premier axe du quartier.

        Returns:
           [Axis]: Une liste contenant les 4 axes générés.
        """
        teta = self.get_angle_between_points(
            axis.start_pos.x, axis.start_pos.y, axis.end_pos.x, axis.end_pos.y)
        seg1 = Axis(axis.end_pos,
                    Point(axis.end_pos.x + 40 * cos(random.uniform(radians(0) + teta, radians(90) + teta)),
                          axis.end_pos.y + 40 * sin(random.uniform(radians(0) + teta, radians(90) + teta))), False)
        seg2 = Axis(axis.end_pos,
                    Point(axis.end_pos.x + 40 * cos(random.uniform(radians(270) + teta, radians(360) + teta)),
                          axis.end_pos.y + 40 * sin(random.uniform(radians(270) + teta, radians(360) + teta))), False)
        seg3 = Axis(axis.start_pos,
                    Point(axis.start_pos.x + 40 * cos(random.uniform(radians(90) + teta, radians(180) + teta)),
                          axis.start_pos.y + 40 * sin(random.uniform(radians(90) + teta, radians(180) + teta))), False)
        seg4 = Axis(axis.start_pos,
                    Point(axis.start_pos.x + 40 * cos(random.uniform(radians(180) + teta, radians(270) + teta)),
                          axis.start_pos.y + 40 * sin(random.uniform(radians(180) + teta, radians(270) + teta))), False)
        return [seg1, seg2, seg3, seg4]

    def global_goals(self, axis):
        """
        Cette fonction va générer deux axes à la fin de l'axe placé en paramètre.
        Les deux axes auront une direction différente.

        Args:
            axis (Axis): L'axe d'origine des deux nouveaux.

        Returns:
            [Axis]: Une liste contenant les deux axes générés.
        """
        teta = self.get_angle_between_points(
            axis.start_pos.x, axis.start_pos.y, axis.end_pos.x, axis.end_pos.y)
        seg1 = Axis(axis.end_pos,
                    Point(axis.end_pos.x + 40 * cos(random.uniform(radians(0) + teta, radians(90) + teta)),
                          axis.end_pos.y + 40 * sin(random.uniform(radians(0) + teta, radians(90) + teta))), False)
        seg2 = Axis(axis.end_pos,
                    Point(axis.end_pos.x + 40 * cos(random.uniform(radians(270) + teta, radians(360) + teta)),
                          axis.end_pos.y + 40 * sin(random.uniform(radians(270) + teta, radians(360) + teta))), False)
        return [seg1, seg2]

    def local_constraints(self, axis, district, polygon_boundary):
        """
        Cette fonction va décider si un axe placé en paramètre peut être ajouté à notre liste d'axes mineurs.
        Elle peut aussi effectuer des changements sur cet axe afin qu'il remplisse les conditions.

        Args:
            axis (Axis): L'axe à tester.
            district (District): Le quartier dans lequel nous travaillons.
            polygon_boundary (Polygon): Un polygone qui représente les limites de la ville.

        Returns:
            bool: Un boolean. True si l'axe peut être ajouté, Faux sinon.
        """
        min_ = 30
        good_point = None
        if not axis.start_pos.within(district.polygon) or not axis.start_pos.within(
                polygon_boundary) or not axis.end_pos.within(polygon_boundary) or not axis.end_pos.within(
            district.polygon):
            return False
        for axis2 in self.axes:
            if axis.start_pos != axis2.end_pos and axis.start_pos != axis2.start_pos and axis.end_pos != axis2.end_pos and axis.end_pos != axis2.start_pos:
                if axis.intersect(axis2):
                    return False
                checker_polygon = self.create_checker_polygon(axis)
                if axis2.start_pos.within(checker_polygon) or axis2.end_pos.within(checker_polygon):
                    if axis.start_pos.distance(LineString([axis2.start_pos, axis2.end_pos])) < min_:
                        good_point = self.find_good_point(
                            axis.start_pos, axis2)
                        min_ = axis.start_pos.distance(good_point)
        if good_point:
            axis.end_pos = good_point
        return True

    @staticmethod
    def find_good_point(point, axis):
        """
        Cette fonction va renvoyer le point de l'axe (donc le point de départ ou le point de fin) le plus
        proche du point placé en paramètres.

        Args:
            point (Point): Un point quelconque.
            axis (Axis): Un axe quelconque.

        Returns:
            Point: Le point le plus de proche de notre paramètre point.
        """
        return axis.start_pos if point.distance(axis.start_pos) < point.distance(axis.end_pos) else axis.start_pos

    @staticmethod
    def create_checker_polygon(axis):
        """
        Crée un polygone autour de l'axe placé en paramètre.
        Ce polygone est souvent utilisé pour vérifier si un point se trouve proche de l'axe placé en paramètre.

        Args:
            axis (Axis): Une axe quelconque.
        Returns:
            Polygone: Le polygone créé.
        """
        hd = Point(axis.end_pos.x + axis.size // 2,
                   axis.end_pos.y - axis.size // 2)
        bg = Point(axis.start_pos.x - axis.size // 2,
                   axis.end_pos.y + axis.size // 2)
        hg = Point(axis.end_pos.x - axis.size // 2,
                   axis.end_pos.y - axis.size // 2)
        bd = Point(axis.start_pos.x + axis.size // 2,
                   axis.start_pos.y + axis.size // 2)
        return Polygon([bg, hg, hd, bd])
