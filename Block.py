
"""
Applies the crossing with edge block with i and j being the coordinates of the upper left corner of the block

..●.
●.●.
.●●●
..●.
"""

def crossing_with_edge(g, i, j):
    for (k,l) in [(0,2), (1, 0), (1, 2), (2,1), (2,2), (2, 3), (3,2)]:
        g.set_occupied(i + k, j + l)
        # g.set_weight() Add later with multiple of delta weights


"""
..●.
...●
....
....
"""
def turn(g, i, j):
    for (k,l) in [(0, 2), (1, 3)]:
        g.set_occupied(i + k, j + l)


"""
..●.
●●●.
.●●●
.●..
"""
def crossing_without_edge(g, i, j):
    for (k,l) in [(0, 2), (1, 0), (1, 1), (1, 2), (2, 1), (2, 2), (2, 3), (3, 1)]:
        g.set_occupied(i + k, j + l)


"""
..●.
..●.
..●.
..●.
"""
def vertical_lign(g, i, j):
    for (k,l) in [(0, 2), (1, 2), (2, 2), (3, 2)]:
        g.set_occupied(i + k, j + l)

"""
....
....
●●●●
....

"""
def horizontal_lign(g, i, j):
    for (k,l) in [(2, 0), (2, 1), (2, 2), (2, 3)]:
        g.set_occupied(i + k, j + l)