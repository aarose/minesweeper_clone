#!/usr/bin/python
from wsgiref.simple_server import make_server
from pyramid.config import Configurator

from grids.routes import routes

if __name__ == '__main__':
    config = Configurator()
    for route in routes:
        config.add_route(route.name, route.url)
        config.add_view(route.view, route_name=route.name)
    app = config.make_wsgi_app()
    server = make_server('0.0.0.0', 8000, app)
    server.serve_forever()
