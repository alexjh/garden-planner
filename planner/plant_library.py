#!/usr/bin/env python3
"""
Library of plant definitions
"""


class PlantLibrary:
    """
    A collection of PlantInfo mapped by names. Filters return lists of names
    """
    def __init__(self, plants):
        self.plants = plants

    def get_seeds_per_square(self, plant):
        """
        Gets the number of seeds / plants per square
        """
        return self.plants[plant].plants_north * self.plants[plant].plants_west

    def get_companions(self, plant):
        """
        Gets the companions for a plant
        """
        return self.plants[plant].companion

    def get_enemies(self, plant):
        """
        Gets the enemies for a plant
        """
        return self.plants[plant].enemy

    def get_trellised(self, names):
        """
        Returns a list of plants that require a trellis
        """
        return [plant
                for plant in self.plants
                if self.plants[plant].trellis and plant in names]

    def get_large_plants(self, names, trellised=False):
        """
        Returns a list of plants that require more than one square
        """
        return [plant
                for plant in self.plants
                if self.plants[plant].size_north > 1 and
                self.plants[plant].size_west > 1 and
                plant in names and
                self.plants[plant].trellis == trellised]
