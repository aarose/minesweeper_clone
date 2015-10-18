#!/usr/bin/python
from pyramid.view import (
    view_config,
    view_defaults,
    )
from pyramid.httpexceptions import (
    HTTPFound,
    HTTPNotFound,
    )

from minesweeper.models_base import DBSession
from minesweeper.grids.models import Game


@view_defaults(route_name='home')
class Home(object):
    def __init__(self, request):
        self.request = request

    @view_config(request_method='GET', renderer='minesweeper:templates/index.html.mako')
    def get(request):
        return {'game': False}

    @view_config(request_method='POST')
    def post(self, request):
        # grid_id = create_game()
        grid_id = 1
        return HTTPFound(location=request.route_url('view_game',
                                                    grid_id=grid_id))


@view_config(route_name='view_game', request_method='GET', http_cache=3600,
             renderer='minesweeper:templates/index.html.mako')
def view_game(request):
    """ Returns the game. """
    game_id = request.matchdict['game_id']
    game = DBSession.query(Game).get(game_id)
    if game is None:
        return HTTPNotFound('No such game.')
    # game = {'contents': [[2, 0], [12, 0]], 'state': 'in-progress'}
    return {'game': True, 'height': 2, 'width': 3}


# view_config(route_name='create_game', request_method='POST', renderer='json')
# def create_game(request):
#    """ Creates a new game. """
    # new_grid = GridManager.create()
    # grid_id = new_grid.id
#    return {'grid_id': 12}


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
