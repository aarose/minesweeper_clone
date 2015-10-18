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
    player_maps = orm.relationship("PlayerMap", backref='player_maps',
                                   order_by="PlayerMap.map_type")
    mine_map = foreign_key_column(None, db.Integer, "mine_maps.id")


class MineMap(ModelBase):
    """ MineMap model. """
    __tablename__ = 'mine_maps'
    id = db.Column(db.Integer, primary_key=True)
    map_data = orm.relationship("MineMapData", backref="map_data",
                                order_by="MineMapData.row_num")
    height = db.Column(db.Integer, nullable=False)
    width = db.Column(db.Integer, nullable=False)

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

    mine_map_id = foreign_key_column(None, db.Integer, "mine_maps.id")
    row_num = db.Column(db.Integer, nullable=False)
    col_num = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        db.PrimaryKeyConstraint('mine_map_id', 'row_num', 'col_num'),
        db.CheckConstraint(row_num >= 0, name='check_row_num_positive'),
        db.CheckConstraint(col_num >= 0, name='check_col_num_positive'),
        {})


class PlayerMap(ModelBase):
    """ PlayerMap model. """
    __tablename__ = 'player_maps'

    id = db.Column(db.Integer, primary_key=True)
    game_id = foreign_key_column(None, db.Integer, "games.id")
    map_type = db.Column(db.Text, nullable=False)
    map_data = orm.relationship("PlayerMapData", backref="map_data",
                                order_by="PlayerMapData.row_num")
    games = orm.relationship("Game", backref="games")

    __table_args__ = (db.UniqueConstraint(game_id, map_type), )

    def to_matrix(self):
        from minesweeper.grids.matrices import Matrix
        mine_map = DBSession.query(MineMap).join(Game).filter_by(
            id=self.game_id).first()
        matrix = Matrix(mine_map.height, mine_map.width)
        for entry in self.map_data:
            # Each entry has a value that needs to be inserted into the matrix
            matrix[entry.row_num][entry.col_num] = entry.value
        return matrix

    def to_list(self, filter_for=None):
        if filter_for is None:
            return [(entry.row_num, entry.col_num) for entry in self.map_data]
        return [(entry.row_num, entry.col_num) for entry in self.map_data if
                entry.value == filter_for]



class PlayerMapData(ModelBase):
    """ Maps a value to a row and column in a Map. """
    __tablename__ = 'player_map_data'

    player_map_id = foreign_key_column(None, db.Integer, "player_maps.id")
    row_num = db.Column(db.Integer, nullable=False)
    col_num = db.Column(db.Integer, nullable=False)
    value = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        db.PrimaryKeyConstraint('player_map_id', 'row_num', 'col_num'),
        db.CheckConstraint(row_num >= 0, name='check_row_num_positive'),
        db.CheckConstraint(col_num >= 0, name='check_col_num_positive'),
        )
