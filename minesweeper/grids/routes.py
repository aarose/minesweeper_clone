#!/usr/bin/python
from collections import namedtuple

from .views import (
    CellView,
    GridCreateView,
    GridDetailView,
    home,
)

Route = namedtuple('Route', ['name', 'url', 'view'])

routes = [
    Route(name='home', url='/', view=home),
    Route(name='grid_create', url='/grid', view=GridCreateView),
    Route(name='grid_get', url='/grid/{grid_id}', view=GridDetailView),
    Route(name='cell', url='/grid/{grid_id}/cell/{x},{y}', view=CellView),
]
