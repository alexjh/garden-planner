from planner.box import Box, get_coords_list

def test_get_coords_list():
    """
    Test get_coords_list()
    """
    coords = get_coords_list(0, 0, 1, 1)
    assert coords == [(0, 0)]

    coords = get_coords_list(0, 0, 2, 2)
    assert coords == [
        (0, 0),
        (0, 1),
        (1, 0),
        (1, 1),
        ]

    coords = get_coords_list(0, 0, 3, 1)
    assert coords == [
        (0, 0),
        (1, 0),
        (2, 0),
        ]

    coords = get_coords_list(0, 0, 1, 3)
    assert coords == [
        (0, 0),
        (0, 1),
        (0, 2),
        ]


def test_box_place_plant():
    Box(4, 4)

    # TODO: Correct placement
    # TODO: Failed placement
