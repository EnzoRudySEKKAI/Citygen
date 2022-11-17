from map.axes import *
from populate.building import Building
from populate.district import District


class City:
    """
    La classe qui représente la ville
    
    Elle à acces à sa taille : width, height
    Son nombre de quartier : nb_districts
    Une liste de ses quartiers : districts
    La limite qui représente la muraille de la ville : boundary
    Des axes majeurs : major_axes
    Le nombre de batiment de la ville: nb_buildings
    """

    #  J'ai pas mis minor axes puisque à terme ça y sera plus
    def __init__(self, nb_districts, city_width, city_height, nb_buildings, districts_types):
        self.city_width = city_width
        self.city_height = city_height
        self.nb_districts = nb_districts
        self.districts = self.generate_districts()
        self.boundary = self.generate_boundary(city_width, city_height)
        self.nb_buildings = nb_buildings
        self.major_axes = Axes()
        self.districts_types = districts_types
        self.area = 0

    def get_axes_list(self):
        """
        Renvoie la liste d'axes contenus dans la ville
        """
        minor_axes = self.get_minor_axes()
        return self.major_axes.axes + minor_axes

    def get_minor_axes(self):
        """
        Renvoie la liste d'axe mineur de la ville.
        """
        minor_axes = []
        for district in self.districts:
            minor_axes.extend(district.axes.axes)
        return minor_axes

    def get_buildings(self):
        """
        Renvoie la liste de batiment de la ville.
        """
        buildings = []
        for district in self.districts:
            buildings.extend(district.buildings)
        return buildings

    @staticmethod
    def generate_boundary(width, height):
        """
        Crée 4 Points aléatoirement dans chaque coins dans la ville pour representer une muraille.

        Args:
            width (int): Largeur de la ville.
            height (int): Hauteur de la ville.

        Returns:
            ndarray: Un tableau np.array contenant les 4 points du représentant les limites de la ville.
        """
        # 
        # H = haut; B = bas ; G =  gauche; D = droit
        tuples_hg = (random.randint(width // 6, width // 4), random.randint(height // 6, height // 4))
        tuples_hd = (random.randint(width - width // 4, width - width // 6), random.randint(height // 6, height // 4))
        tuples_bg = (random.randint(width // 6, width // 4), random.randint(height - height // 4, height - height // 6))
        tuples_bd = (random.randint(width - width // 4, width - width // 6),
                     random.randint(height - height // 4, height - height // 6))
        return np.array([tuples_hg, tuples_hd, tuples_bd, tuples_bg])

    @staticmethod
    def generate_district_centers(nb_district, width, height):
        """
        Genere aleatoirement un nombre de points egal au nombre de quartiers à l'interieur de la muraille.
        Ces points representent les centres des quartiers.

        Args:
            nb_district (int): Le nombre de quartier.
            width (int): La largeur de la ville.
            height (int): La hauteur de la ville.

        Returns:
            ndarray[][]: Un tableau np_array contenant les points des centres des quartiers.
        """
        array = np.zeros([nb_district, 2], np.int32)  # initialisation du tableau de point
        for i in range(nb_district):  # choisir un point aléatoire pour chaques quartiers
            array[i][0] = np.uint16(random.randint(width // 4, width - width // 4))
            array[i][1] = np.uint16(random.randint(height // 4, height - height // 4))
        return array

    def generate_districts(self):
        """
        Genere les differents quartiers.

        Returns:
            [District]: Une liste de quartier.
        """
        district_list = []
        district_centers = self.generate_district_centers(self.nb_districts, self.city_width, self.city_height)
        for i in range(self.nb_districts):
            # Pour l'instant on choisi un type de quartier au hasard parmis 3, à terme les types
            # de qartiers seront dictes par les choix de l'user
            district_type = random.randint(1, 3)
            # on construit un quartier a partir de son type et de son centre
            district_list.append(District(district_type, district_centers[i]))
        return district_list

    def create_major_axes(self):
        """
        Cette fonction actualise l'element major_axes de la ville.
        Elle assigne aussi chaque objet Polygon aux quartiers.
        """
        district_centers = []
        for i in range(self.nb_districts):
            district_centers.append(self.districts[i].get_district_center_as_array())
        polygons = self.major_axes.generate_axes_from_voronoi(self.boundary, district_centers)
        self.assign_polygon_to_district(polygons)

    def create_district_axes(self, district):
        """
        Cette fonction génère les axes mineurs des quartiers.

        Args:
            district (District): Un quartier quelconque.
        """
        district.axes.generate_axes_from_district(district, Polygon(self.boundary))

    def assign_polygon_to_district(self, polygons):
        """
        Permet d'assigner un polygon à un quartier.

        Args:
            polygons (Polygon): Le polygone à assigner.
        """
        for p in polygons:
            for district in self.districts:
                if district.get_district_center_as_point().within(p):
                    district.update_polygon(p)

    def compute_area(self):
        for d in self.districts:
            self.area += d.polygon.area

    def generate_special_building(self, density):
        """
        Cette fonction génère les batiments spéciaux.

        Args:
            density (int): La densité des batiments spéciaux.
        """
        self.compute_area()
        types = self.districts_types
        for district in self.districts:
            factor = len(district.buildings) * float(district.type / 5)
            building_type = Building.HOUSE
            if types['Noble'] >= 1:
                building_type = Building.INN
                types['Noble'] -= 1
            else:
                if types['Magicians'] >= 1:
                    building_type = Building.LIBRARY
                    types['Magicians'] -= 1
                else:
                    if types['Commercial'] >= 1:
                        building_type = Building.MERCHANT
                        types['Commercial'] -= 1
            if len(district.buildings) != 0:
                random.shuffle(district.buildings)
                for i in range(int(factor)):
                    # r = random.randint(0,len(district.buildings)-1)
                    tmp = district.buildings[i]
                    tmp.type = building_type
                    district.buildings[i] = tmp

    def populate(self, district):
        """
        Cette fonction va créer les batiments classiques.

        Args:
            district (District): Le quartier à peupler.
        """
        random.shuffle(district.axes.axes)
        max_bat = self.nb_buildings / self.nb_districts
        for a in range(int(max_bat)):
            if a < len(district.axes.axes):
                district.buildings.append(
                    self.is_building_ok(Building(district.axes.axes[a], 10, Building.HOUSE), district, 10))
        res = [i for i in district.buildings if i.bat_size > 0]
        district.buildings = res

    def is_building_ok(self, building, district, original_bat_size):
        """
        Vérifie qu'un batiment n'est pas placé sur un axe ou sur un autre batiment.
        Si le batiment ne peut pas être placé alors la fonction va être rappelée avec une taille de batiment plus petite
        Args:
            building (Building): Le batiment à vérifier.
            district (District): Le quartier du batiment
            original_bat_size (int): La taille du batiment.

        Returns:
            Building: Le batiment placé, de taille 0 si il n'a pas pu être placé.
        """
        if building.bat_size <= 0:
            return building
        for a in self.major_axes.axes + district.axes.axes:
            if building.is_col_axe(a):
                return self.is_building_ok(
                    Building(building.axe, building.bat_size - (original_bat_size / 5), building.type), district,
                    original_bat_size)
        for b in district.buildings:
            if building.is_col_building(b):
                return self.is_building_ok(
                    Building(building.axe, building.bat_size - (original_bat_size / 5), building.type), district,
                    original_bat_size)
        if (not Polygon(self.boundary).contains(building.polygon)) or (not district.polygon.contains(building.polygon)):
            return self.is_building_ok(
                Building(building.axe, building.bat_size - (original_bat_size / 5), building.type), district,
                original_bat_size)
        else:
            return building
