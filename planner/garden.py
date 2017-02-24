#!/usr/bin/env python3
"""
Manages overall garden layout
"""

from collections import Counter
from random import shuffle, choice
from terminaltables import SingleTable
from yattag import Doc, indent
from box import Box


class GardenLayoutException(Exception):
    """
    Handles unresolvable errors in layout
    """
    pass


class Garden:
    """
    Garden module takes garden size and plant preferences and generates a
    garden layout.

    Boxes are laid out:

                NORTH
        (0,0)            (0,n)
               A  B  C
    WEST                       EAST
               D  E  F
        (m,0)            (m,n)

                SOUTH

    """
    def __init__(self, library, north, west):
        self.library = library
        self.boxes = []
        self.requested = {}
        self.north = north
        self.west = west

        for _ in range(north):
            row = []
            for _ in range(west):
                row.append(Box)
            self.boxes.append(row)

        self.boxes = [([Box() for _ in range(west)]) for _ in range(north)]

    def place_trellised(self):
        """
        Places trellised plants into boxes

        Raises a GardenLayoutException if they can't all be fit.
        """

        # TODO When boxes can be arbitrary sizes, a trellised plant would
        # span the north row, and its size would be 1xn

        trellised = self.library.get_trellised(list(self.requested.keys()))
        shuffle(trellised)

        boxes = [self.boxes[0][i] for i in range(self.west)]
        shuffle(boxes)

        # Get the total number of trellised boxes required, fail early if there
        # isn't enough.
        needed = sum([self.requested[plant] for plant in trellised])
        if int(needed / boxes[0].west) > len(boxes):
            raise GardenLayoutException('Too many trellised plants for boxes')

        # Place the plant in the box and remove it from the requested
        # list
        for plant in trellised:
            while plant in self.requested:
                boxes[0].place_plant(plant, (0, 0), (1, boxes[0].west))
                self.record_placed_plant(plant, boxes[0].west)
                boxes.pop(0)

    def record_placed_plant(self, plant, size):
        """
        Removes a plant from the requested list
        """
        self.requested[plant] -= size
        if self.requested[plant] == 0:
            self.requested.pop(plant)

    def place_large_plants(self):
        """
        Large plants take more than one square. Place them first to make it
        easier

        TODO This should probably sort them into buckets of sizes to make it
        more general.

        TODO 2x2 plants should prefer to be on the edges?
        """
        large = self.library.get_large_plants(list(self.requested.keys()))
        shuffle(large)

        for plant in large:
            size = self.library.get_size(plant)

            boxes = [box
                     for sublist in self.boxes
                     for box in sublist]
            shuffle(boxes)

            for box in boxes:
                coords = box.check_fit(size[0], size[1])
                best = box.find_best_squares(plant,
                                             self.library.get_enemies(plant),
                                             self.library.get_companions(plant),
                                             size,
                                             coords)
                if len(best):
                    box.place_plant(plant, choice(best), size)
                    self.record_placed_plant(plant, size[0]*size[1])
                    break
            else:
                raise GardenLayoutException("Couldn't fit {} into any box".format(plant))

    def place_single_plants(self):
        """
        Places all remaining single square plants
        """
        while len(self.requested):
            plants = list(self.requested.keys())
            shuffle(plants)

            for plant in plants:
                boxes = [box
                         for sublist in self.boxes
                         for box in sublist]
                shuffle(boxes)
                for box in boxes:
                    coords = box.check_fit(1, 1)
                    if len(coords) == 0:
                        continue
                    print('Placing {}, {} squares left, {} plants remaining'.format(plant, self.requested[plant], len(self.requested) - 1))
                    best = box.find_best_squares(plant,
                                                 self.library.get_enemies(plant),
                                                 self.library.get_companions(plant),
                                                 (1, 1),
                                                 coords)
                    if len(best):
                        box.place_plant(plant, choice(best), (1, 1))
                        self.record_placed_plant(plant, 1)
                        break
                else:
                    raise GardenLayoutException("Couldn't fit {} into any box".format(plant))

    def place_beneficials(self):
        """
        Place beneficial plants: marigolds and nasturtiums
        """
        boxes = [box
                 for sublist in self.boxes
                 for box in sublist]

        for box in boxes:
            edges = box.get_edge_squares()
            if len(edges):
                coord = choice(edges)
                box.place_plant('marigold', coord, (1, 1))

        for box in boxes:
            coords = box.check_fit(1, 1)
            if len(coords):
                box.place_plant('nasturtium', choice(coords), (1, 1))

    def generate(self, preferences):
        """
        Generates the garden layout

        preferences is a map of plant names to requested squares
        """
        self.requested = preferences
        self.place_trellised()
        self.place_large_plants()
        self.place_single_plants()
        self.place_beneficials()

    def pprint(self):
        """
        Pretty prints the contents of the box
        """
        table = SingleTable(self.boxes)
        table.inner_heading_row_border = False
        table.inner_row_border = True
        print(table.table)

    def print_boxes(self):
        """
        Prints all boxes in the garden
        """

        boxes = [box
                 for sublist in self.boxes
                 for box in sublist]

        for i in boxes:
            i.pprint()

    def get_seed_summary(self):
        """
        Gets a list of seeds/plants needed
        """
        boxes = [box
                 for sublist in self.boxes
                 for box in sublist]

        squares = []
        for box in boxes:
            box.pprint()

            squares += [square
                        for sublist in box.squares
                        for square in sublist
                        if square is not None]

        plants = Counter(squares)

        seeds = {}
        for plant in plants:
            seeds[plant] = self.library.get_seeds_per_square(plant)*plants[plant]

        return seeds

    def __repr__(self):
        return(indent(self.render_html().getvalue()))

    def render_html(self):
        """
        Prints a box as an HTML table
        """
        doc, tag, text = Doc().tagtext()

        with tag('html'):
            with tag('body'):
                seeds = self.get_seed_summary()
                with tag('ul'):
                    for seed in seeds:
                        with tag('li'):
                            text('{}: {}'.format(seed.capitalize(), seeds[seed]))

                with tag('h2', align='center'):
                    text('North')

                with tag('table', width='100%', border='1px solid black',
                         padding='15px', cellpaddings='15px'):
                    for row in self.boxes:
                        with tag('tr'):
                            for box in row:
                                width = '{}%'.format(int(100/self.west))
                                with tag('td', width=width):
                                    doc.asis(str(box))

                with tag('h2', align='center'):
                    text('South')
        return(doc)

if __name__ == '__main__':
    GARDEN = Garden(None, 3, 5)
    print(GARDEN)
