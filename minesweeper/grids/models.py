#!/usr/bin/python
import sqlalchemy as db
import sqlalchemy.orm as orm

import minesweeper.grids.constants as const
from minesweeper.models_base import (
    DBSession,
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
    player_maps = orm.relationship("PlayerMap", backref='game_id',
                                   order_by="PlayerMap.map_type")
    mine_map = foreign_key_column(None, db.Integer, "mine_maps.id")

    __table_args__ = (
        db.CheckConstraint(state in const.GameState.choices(),
                           name='check_state'),
        {})


class MineMap(ModelBase):
    """ MineMap model. """
    __tablename__ = 'mine_maps'
    id = db.Column(db.Integer, primary_key=True)
    map_data = orm.relationship("MineMapData", backref="map_id",
                                order_by="MineMapData.row_num")
    height = db.Column(db.Integer, nullable=False)
    width = db.Column(db.Integer, nullable=False)

    def __init__(self, height=const.MIN_HEIGHT,
                 width=const.MIN_WIDTH, **kwargs):
        super(MineMap, self).__init__(**kwargs)

    def _validate_init(self, height, width):
        """ Validates input for init. """
        if const.MIN_HEIGHT > height > const.MAX_HEIGHT:
            raise InvalidGrid('Height must be between %s and %s' %
                              (const.MIN_HEIGHT, const.MAX_HEIGHT))
        if const.MIN_WIDTH > width > const.MAX_WIDTH:
            raise InvalidGrid('Width must be between %s and %s' %
                              (const.MIN_WIDTH, const.MAX_WIDTH))

    def to_matrix(self):
        from minesweeper.grids.matrices import MineMatrix
        matrix = MineMatrix(self.height, self.width)
        for entry in self.map_data:
            # Each entry is a mine that needs to be placed in the empty matrix
            matrix.place_mine(entry.row_num, entry.col_num)
        return matrix


class MineMapData(ModelBase):
    """ A Mine's position in a MineMap. """
    __tablename__ = 'mine_map_data'

    map_id = foreign_key_column(None, db.Integer, "mine_maps.id")
    row_num = db.Column(db.Integer, nullable=False)
    col_num = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        db.PrimaryKeyConstraint('map_id', 'row_num', 'col_num'),
        db.CheckConstraint(row_num >= 0, name='check_row_num_positive'),
        db.CheckConstraint(col_num >= 0, name='check_col_num_positive'),
        {})


class PlayerMap(ModelBase):
    """ PlayerMap model. """
    __tablename__ = 'player_maps'

    id = db.Column(db.Integer, primary_key=True)
    game_id = foreign_key_column(None, db.Integer, "games.id")
    map_type = db.Column(db.Text, nullable=False)
    map_data = orm.relationship("PlayerMapData", backref="map_id",
                                order_by="PlayerMapData.row_num")

    __table_args__ = (
        db.CheckConstraint(
            map_type in const.PlayerMapType.choices(),
            name='restrict_map_type'),
        db.UniqueConstraint(game_id, map_type),
        )

    def to_matrix(self):
        from minesweeper.grids.matrices import Matrix
        # TODO: Does this work?
        height = DBSession.query(MineMap.height).join(Game).filter_by(
            game_id=self.game_id)
        width = DBSession.query(MineMap.width).join(Game).filter_by(
            game_id=self.game_id)
        matrix = Matrix(height, width)
        for entry in self.map_data:
            # Each entry has a value that needs to be inserted into the matrix
            matrix[entry.row_num][entry.col_num] = entry.value
        return matrix


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
