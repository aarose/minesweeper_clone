#!/usr/bin/python
import random

import minesweeper.grids.constants as const


class CellStates(object):
    UNCLICKED = 0
    CLUE = [1, 2, 3, 4, 5, 6, 7, 8]
    MINE = 10
    FLAG = 11
    UNSURE = 12


class Matrix(list):
    def __init__(self, height, width=None, init_value=CellStates.UNCLICKED):
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


class InvalidMineAmount(Exception):
    """ Raised when mine limit exceeded. """


class MineMap(Matrix):
    def __init__(self, mine_number, height, width=None,
                 mine_value=CellStates.MINE, **kwargs):
        """
        Creates a Matrix and places mines and clues in it.

        Args:
            mine_number (int): The number of mines to place
            height (int): The number of rows in the matrix.
            width (int, optional): The number of columns in the matrix. If
                not set, defaults to be the same as the height.
            mine_value(int, optional): The value that represents a mine.
                Defaults to CellStates.MINE.
        """
        super(MineMap, self).__init__(height, width=width, **kwargs)
        # Ensure that the number of mines doesn't exceed the number of spaces
        max_mines = int(self.height * self.width * const.MAX_MINE_AREA)
        if mine_number > max_mines:
            raise InvalidMineAmount('%s exceeds the current mine limit of %s'
                                    % (mine_number, max_mines))
        self._place_mines(mine_number, mine_value)

    def _random_coord(self):
        """ Returns random x and y coordinates for this matrix. """
        x = random.randint(0, (self.height - 1))
        y = random.randint(0, (self.width - 1))
        return (x, y)

    def _increment_surrounding(self, focus_x, focus_y, mine_value):
        """
        Increments cells around the given position by 1, if they're not mines.

        Args:
            focus_x (int): The x coordinate of the position (the row).
            focus_y (int): The y coordinate of the position (the column).
            mine_value (int): The value that represents a mine.
        """
        for x in self._adjacent_indices(focus_x, self.height-1):
            for y in self._adjacent_indices(focus_y, self.width-1):
                if (x, y) != (focus_x, focus_y) and self[x][y] != mine_value:
                    self[x][y] += 1

    def _place_mines(self, mine_number, mine_value):
        """ Places mines randomly in the matrix, and set clues around them. """
        for i in range(mine_number):
            placed = False
            while not placed:
                # Generate random position for mine
                (mine_x, mine_y) = self._random_coord()
                # Ensure no mine was already placed there. Overwrite clues.
                if self[mine_x][mine_y] != mine_value:
                    self[mine_x][mine_y] = mine_value
                    self._increment_surrounding(mine_x, mine_y, mine_value)
                    placed = True
