#!/usr/bin/python
from pyramid.response import Response

from ..generic_views import View


class GridView(View):
    allowed_methods = ['get', 'post']

    def get(self):
        """ Returns the serialized grid. """
        # grid_id = self.request.matchdict['grid_id']
        # Find the grid matching the given ID
        # If not found, return HTTP 404
        grid = {'contents': [[2, 0], [12, 0]], 'state': 'in-progress'}
        return Response(str(grid))

    def post(self):
        """ Creates a new grid. """
        # new_grid = GridManager.create()
        # grid_id = new_grid.id
        return Response('New grid created')


class CellView(View):
    allowed_methods = ['get', 'put']

    def get(self):
        """ Returns the value of the cell in the grid, and the game state. """
        # grid_id = self.request.matchdict[grid_id]
        # cell_x = self.request.matchdict['x']
        # cell_y = self.request.matchdict['y']
        # grid = GridManager.get(id=grid_id)
        # Multiply the minemap by the clickmap to get the states, add the
        cell = {'value': 0, 'state': 'in-progress'}
        return Response(str(cell))

    def put(self):
        """ Executes the provided action upon the cell, returns the state. """
        cell = {'value': 2, 'state': 'win'}
        return Response(str(cell))
