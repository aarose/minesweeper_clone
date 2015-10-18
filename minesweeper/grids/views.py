#!/usr/bin/python
import transaction

from pyramid.view import (
    view_config,
    view_defaults,
    )
from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound,
    )

from minesweeper.grids import constants as const
from minesweeper.grids import models
from minesweeper.grids.matrices import MineMatrix
from minesweeper.models_base import DBSession


@view_defaults(route_name='home')
class Home(object):
    def __init__(self, request):
        self.request = request

    @view_config(request_method='GET', renderer=const.MAIN_TEMPLATE)
    def get(self):
        return {'game': False}

    @view_config(request_method='POST')
    def post(self):
        """ Creates a new Game, MineMap, and PlayerMaps. """
        # Create a MineMap
        mine_matrix = MineMatrix(const.DEFAULT_HEIGHT,
                                 width=const.DEFAULT_WIDTH,
                                 mine_number=const.DEFAULT_MINES)
        mine_map = mine_matrix.to_model()
        DBSession.add(mine_map)
        DBSession.flush()

        # Create a Game and PlayerMaps for it
        game = models.Game(mine_map=mine_map.id)
        game.player_maps = [
            models.PlayerMap(map_type=const.PlayerMapType.CLICK),
            models.PlayerMap(map_type=const.PlayerMapType.FLAG),
        ]
        DBSession.add(game)
        DBSession.flush()
        return HTTPFound(location=self.request.route_url('view_game',
                                                         game_id=game.id))


@view_config(route_name='view_game', request_method='GET', http_cache=3600,
             renderer=const.MAIN_TEMPLATE)
def view_game(request):
    """ Returns the game. """
    game_id = request.matchdict['game_id']
    game = DBSession.query(models.Game).get(game_id)
    if game is None:
        return HTTPNotFound('No such game.')

    # game = {'contents': [[2, 0], [12, 0]], 'state': 'in-progress'}
    mine_map = DBSession.query(models.MineMap).get(game.mine_map)
    number_of_mines = DBSession.query(models.MineMapData).filter_by(
        mine_map_id=mine_map.id).count()
    response = {
        'game': True,
        'height': mine_map.height,
        'width': mine_map.width,
        'mines': number_of_mines,
    }
    return response


@view_config(route_name='cell_get', request_method='GET', renderer='json')
def get(request):
    """ Returns the value of the cell in the grid, and the game state. """
    # grid_id = self.request.matchdict[grid_id]
    # cell_x = self.request.matchdict['x']
    # cell_y = self.request.matchdict['y']
    # grid = GridManager.get(id=grid_id)
    # Multiply the minemap by the clickmap to get the states, add the
    cell = {'value': 0, 'state': 'in-progress'}
    return cell


@view_config(route_name='cell_get', request_method='PUT', renderer='json')
def put(request):
    """ Executes the provided action upon the cell, returns the state. """
    cell = {'value': 2, 'state': 'win'}
    return cell
