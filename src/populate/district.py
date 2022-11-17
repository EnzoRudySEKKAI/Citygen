from enum import Enum

from shapely.geometry import Point

from map.axes import Axes

DISTRICTS_TYPE = {
    "Nb_districts": 0,
    "Commercial": 0,
    "Magicians": 0,
    "Noble": 0,
}


# creating enumerations using class
class DistrictTypes(Enum):
    Commercial = 1
    Magicians = 2
    Noble = 3


class District:
    def __init__(self, type, center):
        """
        Constructeur de l'objet District.

        Args:
            type (DistrictTypes): Le type du quartier.
            center ([int]): Le centre du quartier.
            
        Attributes:
            type (DistrictTypes): Le type du quartier.
            center (Point): Le centre du quartier.
            polygon (Polygon): Un polygone représentant le quartier.
            buildings ([Building]): La liste de batiment du quartier.
            axes (Axes): Les axes mineurs du quartier.
            density_factor (int): Le facteur de densité du quartier.
        """
        self.type = type
        DISTRICTS_TYPE[DistrictTypes(type).name] += 1
        self.center = Point(center[0], center[1])
        self.polygon = None
        self.buildings = []
        self.axes = Axes()
        # A CHANGER POUR PLUS TARD FAUT PAS QUE CA SOIT FIXE
        self.density_factor = self.type * 0.2

    def get_district_center_as_point(self):
        return self.center

    def get_district_center_as_array(self):
        return [self.center.x, self.center.y]

    def update_polygon(self, polygon):
        self.polygon = polygon

    def get_polygon(self):
        return self.polygon

    def check(self):
        return self.center.within(self.polygon)

    def add_axes(self, axes):
        self.axes += axes
