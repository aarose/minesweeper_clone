#!/usr/bin/python
import random

from minesweeper.models_base import DBSession
import minesweeper.grids.constants as const
from minesweeper.grids.models import (
    MineMap,
    MineMapData,
    PlayerMap,
    PlayerMapData,
    )


class Matrix(list):
    def __init__(self, height, width=None,
                 init_value=const.CellStates.UNCLICKED):
        """
        Creates a Matrix (nested list).

        Args:
            height (int): The number of rows.
            width (int, optional): The number of columns. If None, will be set
                to the same as the height.
            init_value(int, optional): The value to insert in each position.
                Defaults to CellStates.UNCLICKED.
        """
        if width is None:
            width = height
        value = [[init_value for i in range(width)] for j in range(height)]
        super(Matrix, self).__init__(value)

    @property
    def height(self):
        """ The number of rows. """
        return len(self)

    @property
    def width(self):
        """ The number of columns. """
        return len(self[0])

    def __call__(self, x, y):
        return self[x][y]

    @classmethod
    def _adjacent_indices(cls, index, limit):
        """
        Returns a list of indices - [index - 1, index, index + 1].

        Omits the left or right index if the index is at the edge.
        """
        indices = []
        if index != 0:
            indices.append(index - 1)
        indices.append(index)
        if index != limit:
            indices.append(index + 1)
        return indices

    def to_new_model(self, game, map_type):
        """
        Converts contents into PlayerMapData and a PlayerMap.

        Args:
            game (`grids.models.Game`): The parent Game instance.
            map_type (str): Specifies what type of map. Must be one of
                `grids.constants.PlayerMapType` choices.
        """
        if map_type not in const.PlayerMapType.choices():
            raise Exception('Improper map type "%s"' % map_type)
        player_map = PlayerMap(map_type=map_type, game_id=game.id)

        map_data = []
        for x in range(self.height):
            for y in range(self.width):
                # Only create a data entry (model) for non-zero values
                if self[x][y] != const.CellStates.UNCLICKED:
                    new_data = PlayerMapData(row_num=x, col_num=y,
                                             value=self[x][y])
                    map_data.append(new_data)

        player_map.map_data = map_data
        DBSession.add(player_map)
        DBSession.commit()
        return player_map

    def to_existing_model(self):
        pass


class InvalidMineAmount(Exception):
    """ Raised when mine limit exceeded. """


class MineMatrix(Matrix):
    def __init__(self, height, width=None, mine_number=None,
                 mine_value=const.CellStates.MINE, **kwargs):
        """
        Creates a Matrix and places mines and clues in it.

        Args:
            height (int): The number of rows in the matrix.
            width (int, optional): The number of columns in the matrix. If
                not set, defaults to be the same as the height.
            mine_number (int, optional): The number of mines to randomly place.
                Also places clues around each mine. If left as None, no mines
                Defaults to CellStates.MINE.
            mine_value (int, optional): The value that represents a mine.
                Defaults to CellStates.MINE.
        """
        super(MineMatrix, self).__init__(height, width=width, **kwargs)
        self.mine_value = mine_value
        self.mine_count = 0
        if mine_number is not None:
            if mine_number > self.max_mines:
                raise InvalidMineAmount(
                    '%s exceeds the current mine limit of %s' % (
                        mine_number,
                        self.max_mines,
                    ))

            self._randomly_place_mines(mine_number)

    @property
    def max_mines(self):
        """ The maximum amount of mines that may be placed in this matrix. """
        return int(self.height * self.width * const.MAX_MINE_AREA)

    def _random_coord(self):
        """ Returns random x and y coordinates for this matrix. """
        x = random.randint(0, (self.height - 1))
        y = random.randint(0, (self.width - 1))
        return (x, y)

    def _increment_surrounding(self, focus_x, focus_y):
        """
        Increments cells around the given position by 1, if they're not mines.

        Args:
            focus_x (int): The x coordinate of the position (the row).
            focus_y (int): The y coordinate of the position (the column).
            mine_value (int): The value that represents a mine.
        """
        def is_not_focus(x, y):
            return (x, y) != (focus_x, focus_y)

        for x in self._adjacent_indices(focus_x, self.height-1):
            for y in self._adjacent_indices(focus_y, self.width-1):
                if is_not_focus(x, y) and self[x][y] != self.mine_value:
                    self[x][y] += 1

    def place_mine(self, x, y):
        """
        Places a mine at (x, y).

        Increments the values of the surrounding cells (as long as they're also
        not mines). (These are the clues). Also increments the mine counter.
        """
        # Ensure that adding this mine won't violate the max allowed
        if self.mine_count + 1 > self.max_mines:
            InvalidMineAmount('Cannot place mine - matrix is at maxium '
                              'capacity (%s)' % self.max_mines)
        self[x][y] = self.mine_value
        self.mine_count += 1
        self._increment_surrounding(x, y)  # Add clues

    def _randomly_place_mines(self, mine_number):
        """ Places mines randomly in the matrix, and set clues around them. """
        for i in range(mine_number):
            placed = False
            while not placed:
                # Generate random position for mine
                (mine_x, mine_y) = self._random_coord()
                # Ensure no mine was already placed there. Overwrite clues.
                if self[mine_x][mine_y] != self.mine_value:
                    self.place_mine(mine_x, mine_y)
                    placed = True

    def to_model(self):
        """ Converts contents into MineMapData and a MineMap. """
        mine_map = MineMap(height=self.height, width=self.width)

        mine_data = []
        for x in range(self.height):
            for y in range(self.width):
                # Only create a data entry (model) for mine positions
                if self[x][y] == self.mine_value:
                    new_data = MineMapData(row_num=x, col_num=y)
                    mine_data.append(new_data)

        mine_map.map_data = mine_data
        DBSession.add(mine_map)
        DBSession.commit()
        return mine_map
