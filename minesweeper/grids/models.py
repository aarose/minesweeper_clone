#!/usr/bin/python
from .utils import Matrix, MineMap

MAX_GRID_WIDTH = 100
MAX_GRID_HEIGHT = 100
MAX_MINE_PERCENT = 0.9  # percent, in decimal form
# TODO: fix the way percents work? Calculate max?
MAX_MINE_NUMBER = (MAX_GRID_HEIGHT * MAX_GRID_WIDTH) * MAX_MINE_PERCENT


class InvalidGrid(Exception):
    """ Raised when the grid size or number of mines is not allowed. """


class Grid(object):
    """ Representation of a grid. """
    def __init__(self, width, height, mine_number):
        if width > MAX_GRID_WIDTH:
            raise InvalidGrid('Length cannot exceed %s' % MAX_GRID_WIDTH)
        if height > MAX_GRID_HEIGHT:
            raise InvalidGrid('Height cannot exceed %s' % MAX_GRID_HEIGHT)
        if mine_number > MAX_MINE_NUMBER:
            raise InvalidGrid('Mine number cannot exceed %s' % MAX_MINE_NUMBER)

        self.width = width
        self.height = height
        self.mine_number = mine_number

        # Matrices
        self.mine_map = MineMap(self.mine_number, self.width, self.height)
        self.click_map = Matrix(self.width, self.height)
        self.flag_map = Matrix(self.width, self.height)

    def __str__(self):
        """ Serialization of the grid. """
        return self.__class__

    @property
    def size(self):
        return (self.width, self.height)


class GridManager(object):
    def create(self):
        new_grid = Grid(9, 9)
        new_grid.save()  # commit to the database
        return new_grid
