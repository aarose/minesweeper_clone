#!/usr/bin/python
from collections import namedtuple

from .views import GridView, CellView

Route = namedtuple('Route', ['name', 'url', 'view'])

routes = [
    Route(name='grid', url='/grid', view=GridView),
    Route(name='grid', url='/grid/{id})', view=GridView),
    Route(name='cell', url='/grid/{id}/cell/{x},{y}', view=CellView),
]
