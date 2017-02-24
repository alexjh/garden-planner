#!/usr/bin/env python3

from terminaltables import SingleTable


# A garden contains:
# x y grid of boxes
#
# A box contains:
# x y grid of squares


def create_box_table(box):
    table_instance = SingleTable(box)
    table_instance.inner_heading_row_border = False
    table_instance.inner_row_border = True
    return table_instance

def create_garden_table(garden):
    garden_table = []

    for row in garden:
        garden_row = []
        for box in row:
            garden_row.append(create_box_table(box).table)
        garden_table.append(garden_row)

    table_instance = SingleTable(garden_table)
    table_instance.inner_heading_row_border = False
    table_instance.inner_row_border = True

    return table_instance


if __name__ == '__main__':
    table1 = [
            [1,2,3,4],
            [1,2,3,4],
            [1,2,3,4],
            [1,2,3,4],
            ]
    table2 = [
            ['A','B','C','D'],
            ['A','B','C','D'],
            ['A','B','C','D'],
            ['A','B','C','D'],
            ]
    table3 = [
            ['a','b','c','d'],
            ['a','b','c','d'],
            ['a','b','c','d'],
            ['a','b','c','d'],
            ]
    table4 = [
            ['!','@','#','$'],
            ['!','@','#','$'],
            ['!','@','#','$'],
            ['!','@','#','$'],
            ]

    garden = [[table1, table2], [table3, table4]]


    print(create_box_table(garden[0][0]).table)

    layout = create_garden_table(garden)
    print(layout.table)


