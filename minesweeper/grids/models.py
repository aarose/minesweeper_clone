#!/usr/bin/python
import random

MAX_GRID_LENGTH = 100
MAX_GRID_HEIGHT = 100
MAX_MINE_PERCENT = 0.9  # percent, in decimal form
# TODO: fix the way percents work? Calculate max?
MAX_MINE_NUMBER = (MAX_GRID_HEIGHT * MAX_GRID_LENGTH) * MAX_MINE_PERCENT


class CellStates(object):
    UNCLICKED = 0
    CLUE = [1, 2, 3, 4, 5, 6, 7, 8]
    MINE = 10
    FLAG = 11
    UNSURE = 12


class InvalidGrid(Exception):
    """ Raised when the grid size or number of mines is not allowed. """


class Grid(object):
    """ Representation of a grid. """
    def __init__(self, length, height, mine_number):
        if length > MAX_GRID_LENGTH:
            raise InvalidGrid('Length cannot exceed %s' % MAX_GRID_LENGTH)
        if height > MAX_GRID_HEIGHT:
            raise InvalidGrid('Height cannot exceed %s' % MAX_GRID_HEIGHT)
        if mine_number > MAX_MINE_NUMBER:
            raise InvalidGrid('Mine number cannot exceed %s' % MAX_MINE_NUMBER)
        self.length = int(length)
        self.height = int(height)
        self.mine_number = mine_number
        self.mine_map = self._create_mine_map()
        self.click_map = self._empty_matrix()
        self.flag_map = self._empty_matrix()

    def __str__(self):
        """ Serialization of the grid. """
        return self.__class__

    @property
    def size(self):
        return (self.length, self.height)

    def _empty_matrix(self):
        """ Returns an empty matrix, with all cells in an unclicked state."""
        return [[CellStates.UNCLICKED for i in xrange(self.length)]
                for j in xrange(self.height)]

    def _create_mine_map(self):
        """ Returns a mine map, with mines and clues. """
        mine_map = self._empty_matrix()
        self._place_mines(mine_map)

    def _place_mines(self, mine_map):
        """ Place mines randomly in the mine_map matrix. """
        for i in xrange(self.mine_number):
            placed = False
            while not placed:
                # Generate random position for mine
                mine_x = random.randint(0, (self.length - 1))
                mine_y = random.randint(0, (self.height - 1))
                # Ensure no mine was already placed there
                if not mine_map[mine_x][mine_y]:  # will be 0 if no mine
                    mine_map[mine_x][mine_y] = CellStates.MINE
                    placed = True


class GridManager(object):
    def create(self):
        new_grid = Grid(9, 9)
        new_grid.save()  # commit to the database
        return new_grid
