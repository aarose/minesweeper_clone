#!/usr/bin/python
from .utils import (
    MAX_MINE_AREA,
    Matrix,
    MineMap,
)

MAX_GRID_WIDTH = 30
MAX_GRID_HEIGHT = 30


class InvalidGrid(Exception):
    """ Raised when the grid size or number of mines is not allowed. """


class Grid(object):
    """ Representation of a grid. """
    def __init__(self, height, width, mine_number):
        if height > MAX_GRID_HEIGHT:
            raise InvalidGrid('Height cannot exceed %s' % MAX_GRID_HEIGHT)
        if width > MAX_GRID_WIDTH:
            raise InvalidGrid('Width cannot exceed %s' % MAX_GRID_WIDTH)
        mine_limit = int(height * width * MAX_MINE_AREA)
        if mine_number > mine_limit:
            raise InvalidGrid('Mine number cannot exceed %s' % mine_limit)

        self.width = width
        self.height = height
        self.mine_number = mine_number

        # Matrices
        self.mine_map = MineMap(mine_number, height, width)
        self.click_map = Matrix(height, width)
        self.flag_map = Matrix(height, width)

    def __str__(self):
        """ Serialization of the grid. """
        # TODO:
        return self.__class__

    def save(self):
        """ Commit to the database. """
        # TODO

    @property
    def size(self):
        return (self.width, self.height)


class GridManager(object):
    def create(self):
        new_grid = Grid(9, 9)
        # TODO:
        new_grid.save()  # commit to the database
        return new_grid
