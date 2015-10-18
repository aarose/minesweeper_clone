#!/usr/bin/python
from pyramid.view import view_config


@view_config(route_name='home', request_method='GET', http_cache=3600,
             renderer='minesweeper:templates/index.html.mako')
def home(request):
    return {}


@view_config(route_name='game_get', request_method='GET', renderer='json')
def view_game(self):
    """ Returns the serialized grid for this game, and game state. """
    # grid_id = self.request.matchdict['grid_id']
    # Find the grid matching the given ID
    # If not found, return HTTP 404
    grid = {'contents': [[2, 0], [12, 0]], 'state': 'in-progress'}
    return grid


@view_config(route_name='game_create', request_method='POST', renderer='json')
def create_game(self):
    """ Creates a new game. """
    # new_grid = GridManager.create()
    # grid_id = new_grid.id
    return {'grid_id': 12}


@view_config(route_name='cell_get', request_method='GET', renderer='json')
def get(self):
    """ Returns the value of the cell in the grid, and the game state. """
    # grid_id = self.request.matchdict[grid_id]
    # cell_x = self.request.matchdict['x']
    # cell_y = self.request.matchdict['y']
    # grid = GridManager.get(id=grid_id)
    # Multiply the minemap by the clickmap to get the states, add the
    cell = {'value': 0, 'state': 'in-progress'}
    return cell


@view_config(route_name='cell_get', request_method='PUT', renderer='json')
def put(self):
    """ Executes the provided action upon the cell, returns the state. """
    cell = {'value': 2, 'state': 'win'}
    return cell
