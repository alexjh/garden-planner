#!/usr/bin/env python3
"""
Helpers for asking questions about the garden
"""

from prompt_toolkit import prompt
from prompt_toolkit.validation import Validator, ValidationError
from prompt_toolkit.contrib.completers import WordCompleter


class PlantNameValidator(Validator):
    """
    Ensures the plant name is valid
    """

    def __init__(self, names):
        self.names = names

    def validate(self, document):
        text = document.text

        if text not in self.names and text != '':
            raise ValidationError(message='{} is not a valid plant name'.
                                  format(text))

class NumberValidator(Validator):
    """
    Ensures prompt is a number
    """
    def validate(self, document):
        text = document.text

        if not text or (text and not text.isdigit()):
            raise ValidationError(message='This input contains non-numeric characters')


class PlantSquareValidator(Validator):
    """
    Ensures prompt is a number and it fits in the squares required for this
    plant
    """
    def __init__(self, size):
        self.size = size

    def validate(self, document):
        text = document.text

        if not text or (text and not text.isdigit()):
            raise ValidationError(message='This input contains non-numeric characters')
        elif (int(text) % self.size) != 0:
            raise ValidationError(message='This plant needs to have a multiple of {} squares'.format(self.size))


def get_north_boxes():
    """
    Prompt for the boxes in the north/south direction
    """
    answer = prompt('Number of boxes in the north/south direction: ',
                    validator=NumberValidator())
    return int(answer)


def get_west_boxes():
    """
    Prompt for the boxes in the west/east direction
    """
    answer = prompt('Number of boxes in the east/west direction: ',
                    validator=NumberValidator())
    return int(answer)


def get_plant(plant_names):
    """
    Gets a plant to choose
    """

    completer = WordCompleter(plant_names)
    validator = PlantNameValidator(plant_names)
    text = prompt('Select a plant: ', completer=completer,
                  validator=validator)
    return text


def get_plant_squares(plant, squares, north=1, west=1):
    """
    Prompt for the squares to devote to this plant
    """

    validator = PlantSquareValidator(north * west)
    answer = prompt('Number of squares for {} ({} remaining): '.format(plant, squares),
                    validator=validator)
    return int(answer)


def get_plant_trellises(plant, trellis):
    """
    Prompt for number of trellises for a plant
    """
    print('{} is grown on a trellis, enter number of *trellises* to use'.
          format(plant))
    print('{} trellises available'.format(trellis))
    answer = prompt('Number of trellises: ', validator=NumberValidator())
    return int(answer)*4, int(answer)


def get_plant_list(plants, squares, trellis):
    """
    Queries for all of the plant names and their amounts
    """

    plant_list = {}
    names = list(sorted(plants.keys()))

    while True:
        plant_name = get_plant(names)
        if plant_name == '' or squares == 0:
            break

        if plants[plant_name].trellis:
            if trellis != 0:
                plant_squares, trellis_used = get_plant_trellises(plant_name, trellis)
                trellis -= trellis_used
            else:
                print('{} requires a trellis, but no trellises available'.format(plant_name))
        else:
            plant_squares = get_plant_squares(plant_name, squares,
                                              *plants[plant_name].get_size())
        if plant_squares != 0:
            plant_list[plant_name] = plant_squares

        squares -= plant_squares

    return plant_list
