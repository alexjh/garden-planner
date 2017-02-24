#!/usr/bin/env python3
"""
Model for PlantInfo

Contains planting details like spacing, beneficial/negative neighbours
"""

def _get_config(config, name, default):
    if name in config:
        return config[name]
    else:
        return default

class PlantInfo:
    def __init__(self, name, config):
        self.name = name
        self.enemy = _get_config(config, 'enemy', [])
        self.companion = _get_config(config, 'companion', [])
        self.plants_north = _get_config(config, 'plants_north', 1)
        self.plants_west = _get_config(config, 'plants_west', 1)
        self.size_north = _get_config(config, 'size_north', 1)
        self.size_west = _get_config(config, 'size_west', 1)
        self.height = _get_config(config, 'height', 'short')
        self.trellis = _get_config(config, 'trellis', False)

    def get_size(self):
        """
        Gets the north and west size of the plant
        """
        return self.size_north, self.size_west

    def get_plants_per_square(self):
        """
        Gets the number of plants per square
        """
        return self.plants_north * self.plants_west
