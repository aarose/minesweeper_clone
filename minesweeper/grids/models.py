#!/usr/bin/python
from .utils import (
    MAX_MINE_AREA,
    Matrix,
    MineMap,
)

MAX_GRID_WIDTH = 30
MAX_GRID_HEIGHT = 30


class GameState(object):
    IN_PROGRESS = 0
    WIN = 1
    LOSE = -1


class InvalidGrid(Exception):
    """ Raised when the grid size or number of mines is not allowed. """


class Game(object):
    """ Representation of a game. """
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
        self.state = GameState.IN_PROGRESS

        # Matrices
        self.mine_map = MineMap(mine_number, height, width)
        self.click_map = Matrix(height, width)
        self.flag_map = Matrix(height, width)

    def __str__(self):
        """ Serialization of the Game. """
        # TODO:
        return self.__class__

    def save(self):
        """ Commit to the database. """
        # TODO

    @property
    def size(self):
        return (self.width, self.height)


class GameManager(object):
    def create(self):
        new_game = Game(9, 9)
        # TODO:
        new_game.save()  # commit to the database
        return new_game
