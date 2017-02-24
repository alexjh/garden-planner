#!/usr/bin/env python3
"""
Garden planner
"""
import sys
import pprint
import yaml
from garden import Garden
from plant_info import PlantInfo
from plant_library import PlantLibrary
import planner_ui

# TODO Make each box customizable
SQUARES_PER_BOX = 16


def load_plants_db(filename):
    # TODO handle missing file
    # TODO handle invalid yaml data
    with open(filename) as plants_doc:
        plants_yaml = yaml.load(plants_doc)
    return {p: PlantInfo(p, plants_yaml[p]) for p in plants_yaml}


def get_garden_details():
    """
    Queries for the garden size
    """
    north = planner_ui.get_north_boxes()
    west = planner_ui.get_west_boxes()
    return north, west


def get_plant_preferences(plants, squares, trellis):
    """
    Plant preferences are a map of plants to number of squares in garden
    """
    return planner_ui.get_plant_list(plants, squares, trellis)


def generate_garden_layout(library, north, west, plant_prefs):
    """
    Generate a list of boxes, containing a list of squares with plant names
    """

    garden = Garden(library, north, west)
    garden.generate(plant_prefs)

    return garden


def main():
    """
    Garden planner control
    """

    # Load the plants db
    plants = load_plants_db('plants.yaml')
    plant_library = PlantLibrary(plants)

    # Query for garden details
    north, west = get_garden_details()

    # Query for plant details
    plant_prefs = get_plant_preferences(plants, north*west*SQUARES_PER_BOX, west)

    # Generate the layout
    garden_layout = generate_garden_layout(plant_library, north, west,
                                           plant_prefs)

    # Display the grid
    html = garden_layout.render_html()
    sys.stderr.write(html.getvalue())

if __name__ == '__main__':
    main()
