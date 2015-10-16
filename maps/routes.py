from collections import namedtuple

from .views import create_grid, get_grid, get_cell

Route = namedtuple('Route', ['name', 'url', 'view'])

routes = [
    Route(name='grid', url='/grid', view=create_grid),
    Route(name='grid', url='/grid/{id})', view=get_grid),
    Route(name='cell', url='/grid/{id}/cell/{x},{y}', view=get_cell),
]
