#!/usr/bin/env python3
"""
Class for managing boxes
"""


from random import shuffle, choice
from terminaltables import SingleTable
from yattag import Doc


def get_coords_list(north, west, size_north, size_west):
    """
    Translates an origin + size to a list of coordinates
    """
    coords = []

    for i in range(size_north):
        for j in range(size_west):
            coords.append((north + i, west + j))

    return coords


class Box:
    """
    A box contains 4 x 4 squares
    """

    def __init__(self, north=4, west=4):
        self.north = north
        self.west = west
        self.squares = [([None] * west) for _ in range(north)]

    def place_plant(self, name, origin, dimensions):
        """
        Places a plant into the squares according to its size
        """
        for i in range(dimensions[0]):
            for j in range(dimensions[1]):
                self.squares[i+origin[0]][j+origin[1]] = name

    def find_best_squares(self, plant, enemies, companions, dimensions, coords):
        """
        Finds a list of the best squares according to their fitness
        """
        rankings = self.sort_squares(plant, enemies, companions, dimensions,
                                     coords)

        best = list(rankings.keys())
        best.sort()

        return rankings[best[0]]

    def sort_squares(self, plant, enemies, companions, dimensions, coords):
        """
        Puts coordinates into bins depending on their fitness
        """
        rankings = {}

        for coord in coords:
            rank = self.rank_square(plant, enemies, companions, coord,
                                    dimensions)

            if rank not in rankings:
                rankings[rank] = []

            rankings[rank].append(coord)

        return rankings

    def rank_square(self, plant, enemies, companions, origin, dimensions):
        """
        Provides a ranking for the plant based on it's neighbours
        """

        rank = 0

        # Avoid placing plants together as it increases the chance of pest
        # infestation
        enemies += plant

        for neighbour in self.get_neighbours(origin, dimensions):
            if self.squares[neighbour[0]][neighbour[1]] in enemies:
                rank -= 1
            elif self.squares[neighbour[0]][neighbour[1]] in companions:
                rank += 1

        return rank

    def get_coord_neighbours(self, coord):
        """
        Get list of neighbours to the coordinate that are inside the box.
        """
        neighbours = [
            (coord[0] - 1, coord[1] - 1),
            (coord[0], coord[1] - 1),
            (coord[0] + 1, coord[1] - 1),
            (coord[0] - 1, coord[1]),
            (coord[0] + 1, coord[1]),
            (coord[0] - 1, coord[1] + 1),
            (coord[0], coord[1] + 1),
            (coord[0] + 1, coord[1] + 1)
        ]

        return [c
                for c in neighbours
                if c[0] >= 0 and
                c[1] >= 0 and
                c[0] < self.north and
                c[1] < self.west]

    def get_neighbours(self, origin, dimensions):
        """
        Gets a list of coordinates that are connected to this footprint
        """
        own_coords = get_coords_list(origin[0], origin[1], dimensions[0],
                                     dimensions[1])
        coords = []
        for coord in own_coords:
            for i in self.get_coord_neighbours(coord):
                if i not in own_coords:
                    coords.append(i)
        return coords

    def get_plants_in_location(self, coords):
        """
        Gets a list of plant names from the list of coordinates.
        """
        return [self.squares[coord[0]][coord[1]]
                for coord in coords
                if self.squares[coord[0]][coord[1]] is not None]

    def check_empty(self, origin, size_north=1, size_west=1):
        """
        Check if a coordinate + size are all empty
        """

        # Can't be empty if it's bigger than the box
        if size_north > self.north or size_west > self.west:
            return False

        for coord in get_coords_list(origin[0], origin[1],
                                     size_north, size_west):
            if self.squares[coord[0]][coord[1]] != None:
                return False

        return True

    def check_fit(self, size_north, size_west):
        """
        Returns a list of coordinates where the plant would fit into this box.
        """
        coords = []

        for i in range(self.north):
            for j in range(self.west):
                if self.check_empty((i, j), size_north, size_west):
                    coords.append((i, j))

        return coords

    def get_edge_squares(self, empty=True):
        """
        Gets list of empty edge squares
        """

        edges = []

        # Top edge
        for i in range(self.north):
            if not empty or self.squares[i][0] is None:
                edges.append((i, 0))

        # Sides
        for i in (0, self.west - 1):
            if not empty or self.squares[0][i] is None:
                edges.append((0, i))

            if not empty or self.squares[self.north - 1][i] is None:
                edges.append((self.north - 1, i))

        # Bottom edge
        for i in range(self.north):
            if not empty or self.squares[i][self.west - 1] is None:
                edges.append((i, self.west - 1))

        return edges

    def pprint(self):
        """
        Pretty prints the contents of the box
        """
        table = SingleTable(self.squares)
        table.inner_heading_row_border = False
        table.inner_row_border = True
        print(table.table)

    def __repr__(self):
        return self.render_html().getvalue()

    def render_html(self):
        """
        Prints a box as an HTML table
        """
        doc, tag, text = Doc().tagtext()

        with tag('table', border='1px solid black', width='100%'):
            for row in self.squares:
                with tag('tr'):
                    for square in row:
                        width = '{}%'.format(int(100/self.west))
                        with tag('td', align='center', width=width):
                            if square is not None:
                                doc.stag('br')
                                text(square.capitalize())
                                doc.stag('br')
                            else:
                                doc.stag('br')
                                doc.asis('&nbsp;')
                                doc.stag('br')
        return doc

if __name__ == '__main__':
    BOX = Box()
    BOX.place_plant('carrot', (0, 0), (1, 2))
    print(BOX)
