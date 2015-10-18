#!/usr/bin/python
MAIN_TEMPLATE = 'minesweeper:templates/index.html.mako'

DEFAULT_HEIGHT = 9
DEFAULT_WIDTH = 9
DEFAULT_MINES = 10

MIN_HEIGHT = 2
MAX_HEIGHT = 30

MIN_WIDTH = 2
MAX_WIDTH = 30

MIN_MINE_NUM = 1
MAX_MINE_AREA = 0.7


class CellStates(object):
    UNCLICKED = 0
    CLUE = [1, 2, 3, 4, 5, 6, 7, 8]
    MINE = 10
    FLAG = 11
    UNSURE = 12


class GameState(object):
    IN_PROGRESS = 0
    WIN = 1
    LOSE = -1

    @classmethod
    def choices(cls):
        return [cls.IN_PROGRESS, cls.WIN, cls.LOSE]


class PlayerMapType(object):
    CLICK = 'click'
    FLAG = 'flag'

    @classmethod
    def choices(cls):
        return [cls.CLICK, cls.FLAG]


class PlayerMapDataValue(object):
    UNCLICKED = 0  # Used to mask MineMap values
    CLICKED = 1  # Reveal MineMap value
    FLAG = 11
    UNSURE = 12

    @classmethod
    def choices(cls):
        return [cls.UNCLICKED, cls.UNCLICKED, cls.FLAG, cls.UNSURE]


class MineMapDataValue(object):
    CLUE = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    MINE = 10

    @classmethod
    def choices(cls):
        return cls.CLUE + [cls.MINE]
