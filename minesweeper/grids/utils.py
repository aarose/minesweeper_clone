#!/usr/bin/python
import random

class CellStates(object):
    UNCLICKED = 0
    CLUE = [1, 2, 3, 4, 5, 6, 7, 8]
    MINE = 10
    FLAG = 11
    UNSURE = 12


class Matrix(list):
    def __init__(self, length, height=None, init_value=None):
        if height is None:
            return [[init_value for i in xrange(length)]
                    for j in xrange(length)]
        return [[init_value for i in xrange(length)] for j in xrange(height)]


class MineMap(Matrix):
    def __init__(self, *args, **kwargs):
        super(MineMap, self).__init__(*args, **kwargs)


def create_mine_map(self, length, height):
    """ Returns a mine map, with mines and clues. """
    mine_map = Matrix(length, height)
    place_mines(mine_map)


def place_mines(self, matrix, mine_number):
    """ Place mines randomly in the matrix. """
    for i in xrange(self.mine_number):
        placed = False
        while not placed:
            # Generate random position for mine
            mine_x = random.randint(0, (self.length - 1))
            mine_y = random.randint(0, (self.height - 1))
            # Ensure no mine was already placed there
            if not matrix[mine_x][mine_y]:  # will be 0 if no mine
                matrix[mine_x][mine_y] = CellStates.MINE
                placed = True
    return matrix


class GridManager(object):
    def create(self):
        new_grid = Grid(9, 9)
        new_grid.save()  # commit to the database
        return new_grid
