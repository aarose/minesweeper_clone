#!/usr/bin/python
import sqlalchemy as db
import sqlalchemy.orm as orm

import minesweeper.grids.constants as const
from minesweeper.models_base import (
    ModelBase,
    foreign_key_column,
    )


class InvalidGrid(Exception):
    """ Raised when the grid size or number of mines is not allowed. """


class Game(ModelBase):
    """ Representation of a game session. """
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.Integer, default=const.GameState.IN_PROGRESS,
                      nullable=False)
    player_maps = orm.relationship("PlayerMap", order_by="PlayerMap.map_type")
    mine_map = foreign_key_column(None, db.Integer, "mine_maps.id")

    __table_args__ = (
        db.CheckConstraint(state in const.GameState.choices(),
                           name='check_state'),
        {})

    def _validate_init(self, height, width, mine_number):
        """ Validates input for init. """
        if const.MIN_GRID_HEIGHT > height > const.MAX_GRID_HEIGHT:
            raise InvalidGrid('Height must be between %s and %s' %
                              (const.MIN_GRID_HEIGHT, const.MAX_GRID_HEIGHT))
        if const.MIN_GRID_WIDTH > width > const.MAX_GRID_WIDTH:
            raise InvalidGrid('Width must be between %s and %s' %
                              (const.MIN_GRID_WIDTH, const.MAX_GRID_WIDTH))
        mine_limit = int(height * width * const.MAX_MINE_AREA)
        if const.MIN_MINE_NUM > mine_number > mine_limit:
            raise InvalidGrid('Mine number cannot exceed %s' % mine_limit)

    def __init__(self, height=const.MIN_GRID_HEIGHT, width=None,
                 mine_number=const.MIN_MINE_NUM):
        if width is None:
            width = height
        self._validate_init(height, width, mine_number)
        super(Game, self).__init__(height=height,
                                   width=width,
                                   mine_number=mine_number,
                                   )

        # Matrices - TODO: One to one with Game
        # self.mine_map = MineMap(mine_number, height, width)
        # self.click_map = Matrix(height, width)
        # self.flag_map = Matrix(height, width)


class MineMap(ModelBase):
    """ MineMap model. """
    __tablename__ = 'mine_maps'
    id = db.Column(db.Integer, primary_key=True)
    map_data = orm.relationship("MineMapData", backref="mine_maps",
                                order_by="MineMapData.row_num")


class MineMapData(ModelBase):
    """ Maps values to rows and cols in a MineMap. """
    __tablename__ = 'mine_map_data'

    map_id = foreign_key_column(None, db.Integer, "mine_maps.id")
    row_num = db.Column(db.Integer, nullable=False)
    col_num = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        db.PrimaryKeyConstraint('map_id', 'row_num', 'col_num'),
        db.CheckConstraint(row_num >= 0, name='check_row_num_positive'),
        db.CheckConstraint(col_num >= 0, name='check_col_num_positive'),
        db.CheckConstraint(value in const.MineMapDataValue.choices()),
        {})


class PlayerMap(ModelBase):
    """ PlayerMap model. """
    __tablename__ = 'player_maps'

    id = db.Column(db.Integer, primary_key=True)
    game_id = foreign_key_column(None, db.Integer, "games.id")
    map_type = db.Column(db.Text, nullable=False)
    map_data = orm.relationship("PlayerMapData", backref="player_maps",
                                order_by="PlayerMapData.row_num")

    __table_args__ = (
        db.CheckConstraint(
            map_type in const.PlayerMapType.choices(),
            name='restrict_map_type'),
        db.UniqueConstraint(game_id, map_type),
        )


class PlayerMapData(ModelBase):
    """ Maps a value to a row and column in a Map. """
    __tablename__ = 'player_map_data'

    map_id = foreign_key_column(None, db.Integer, "player_maps.id")
    row_num = db.Column(db.Integer, nullable=False)
    col_num = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        db.PrimaryKeyConstraint('map_id', 'row_num', 'col_num'),
        db.CheckConstraint(row_num >= 0, name='check_row_num_positive'),
        db.CheckConstraint(col_num >= 0, name='check_col_num_positive'),
        db.CheckConstraint(value in const.PlayerMapDataValue.choices(),
                           name='check_value'),
        {})
