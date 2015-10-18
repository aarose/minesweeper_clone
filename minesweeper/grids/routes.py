#!/usr/bin/python
from collections import namedtuple

Route = namedtuple('Route', ['name', 'url'])

routes = [
    Route(name='home', url='/'),
    Route(name='game_create', url='/grid'),
    Route(name='game_get', url='/grid/{grid_id}'),
    Route(name='cell_get', url='/grid/{grid_id}/cell/{x},{y}'),
]
