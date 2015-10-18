#!/usr/bin/python
from collections import namedtuple

Route = namedtuple('Route', ['name', 'url'])

routes = [
    Route(name='home', url='/'),
    Route(name='create_game', url='/game'),
    Route(name='view_game', url='/game/{game_id}'),
    Route(name='cell_get', url='/game/{game_id}/cell/{x},{y}'),
    Route(name='get_flags', url='/game/{game_id}/flags'),
]
