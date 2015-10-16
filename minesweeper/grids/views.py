#!/usr/bin/python
from pyramid.response import Response

from ..generic_views import View


class GridView(View):
    allowed_methods = ['get', 'post']

    def get(self):
        """ Returns the serialized grid. """
        # grid_id = self.request.matchdict['id']
        grid = {'contents': [[2, 0], [12, 0]], 'state': 'in-progress'}
        return Response(str(grid))

    def post(self):
        """ Creates a new grid. """
        return Response('New grid created')


class CellView(View):
    allowed_methods = ['get', 'put']

    def get(self):
        """ Returns the value of the cell in the grid, and the game state. """
        cell = {'value': 0, 'state': 'in-progress'}
        return Response(str(cell))

    def put(self):
        """ Executes the provided action upon the cell, returns the state. """
        cell = {'value': 2, 'state': 'win'}
        return Response(str(cell))
