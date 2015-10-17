#!/usr/bin/python
from pyramid.config import Configurator
from sqlalchemy import engine_from_config

from .models_base import (
    DBSession,
    Base,
)
from minesweeper.grids.routes import routes


def main(global_config, **settings):
    # Set up database stuff
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine

    # Configure
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    for route in routes:
        config.add_route(route.name, route.url)
        config.add_view(route.view, route_name=route.name)
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.scan()
    return config.make_wsgi_app()
