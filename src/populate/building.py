import random as rd
from math import *

from shapely.geometry import Polygon, Point, LineString


class Building:
    HOUSE = {
        "Color": (0, 0, 255),
        "Scale": 1.,
        "Thickness": 1
    }
    LIBRARY = {
        "Color": (102, 51, 0),
        "Scale": 1.2,
        "Thickness": 1
    }
    MERCHANT = {
        "Color": (0, 0, 0),
        "Scale": 1.3,
        "Thickness": 1
    }
    INN = {
        "Color": (0, 255, 255),
        "Scale": 1.3,
        "Thickness": 1
    }

    def __init__(self, axe, bat_size, type_):
        self.type = type_
        self.bat_size = bat_size
        self.axe = axe
        self.polygon = self.create_building(axe, bat_size)

    def create_building(self, axe, bat_size):
        """
        Une fonction qui crée un batiment par rapport à un axe placé en paramètre.

        Args:
            axe (Axis): Un axe quelconque.
            bat_size (int): La taille du batiment.

        Returns:
            Polygon: Un object Polygon représentant le batiment.
        """
        bool_ = rd.randint(0, 1)

        if bool_ == 1:
            x_a = axe.start_pos.x
            y_a = axe.start_pos.y
            x_b = axe.end_pos.x
            y_b = axe.end_pos.y
        else:
            x_a = axe.end_pos.x
            y_a = axe.end_pos.y
            x_b = axe.start_pos.x
            y_b = axe.start_pos.y

        theta = self.get_angle_between_points(x_a, y_a, x_b, y_b)
        theta_prime = theta + radians(90)
        c = self.random_point_on_a_segment(x_a, y_a, x_b, y_b)
        distance = rd.uniform(0.4, 30 - bat_size)
        bl_building_corner = Point(c.x + distance * cos(theta_prime), c.y + distance * sin(theta_prime))
        br_building_corner = Point(bl_building_corner.x + bat_size * cos(theta),
                                   bl_building_corner.y + bat_size * sin(theta))
        ur_building_corner = Point(br_building_corner.x + bat_size * cos(theta_prime),
                                   br_building_corner.y + bat_size * sin(theta_prime))
        ul_building_corner = Point(bl_building_corner.x + bat_size * cos(theta_prime),
                                   bl_building_corner.y + bat_size * sin(theta_prime))
        building_polygon = Polygon([bl_building_corner, br_building_corner, ur_building_corner, ul_building_corner])

        return building_polygon

    @staticmethod
    def random_point_on_a_segment(x_orig, y_orig, x_end, y_end):
        """
        Fonction qui place un point de manière aléatoire sur un axe.

        Args:
            x_orig (int): Coordonnées du premier point sur l'axe des abscisses.
            y_orig (int): Coordonnées du premier point sur l'axe des ordonnées.
            x_end (int): Coordonnées du deuxième point sur l'axe des abscisses.
            y_end (int): Coordonnées du deuxième point sur l'axe des ordonnées.
        Returns:
            Point: Le point placé sur le segment.
        """
        n = rd.random()
        if x_orig != x_end and y_orig != y_end:
            slope = (y_end - y_orig) / (x_end - x_orig)
            x = (x_end - x_orig) * n + x_orig
            y = slope * (x - x_orig) + y_orig
        else:
            if x_orig == x_end and y_orig != y_end:
                x = x_orig
                y = (y_end - y_orig) * n + y_orig
            else:
                y = y_orig
                x = (x_end - x_orig) * n + x_orig
        return Point(x, y)

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

    def is_col_axe(self, axe):
        """"
        Collision entre un bâtiment et un axe
        (true,false)
        """
        a = Point(axe.start_pos.x, axe.start_pos.y)
        b = Point(axe.end_pos.x, axe.end_pos.y)
        axe = LineString([a, b])
        return self.polygon.intersects(axe)

    def is_col_building(self, building_2):
        """"
        Collision entre un batiment et
        un autre batiment (true,false)
        """
        return self.polygon.intersects(building_2.polygon)
