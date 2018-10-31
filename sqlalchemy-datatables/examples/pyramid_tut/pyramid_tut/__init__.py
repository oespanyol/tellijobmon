"""Initialize application."""
from datetime import date

from pyramid.config import Configurator
from pyramid.renderers import JSON
from sqlalchemy import engine_from_config

from .models import Base, DBSession


def date_adapter(obj, request):
    return str(obj)


def main(global_config, **settings):
    """Return a Pyramid WSGI application."""
    engine = engine_from_config(settings, 'sqlalchemy.')
    DBSession.configure(bind=engine)
    Base.metadata.bind = engine
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.include('pyramid_debugtoolbar')
    config.add_route('home', '/')
    config.add_route('recipients', '/recipients')
    config.add_route('recipients_data', '/recipients_data')
    config.add_route('jobs', '/jobs')
    config.add_route('jobs_data', '/jobs_data')
    config.add_route('job', '/job')
    config.add_route('show_job', '/show_job/{id}')
    config.add_route('files', '/files')
    config.add_route('files_data', '/files_data')
    config.add_route('file', '/file')
    config.add_route('show_file', '/show_file/{id}')

    config.add_route('monitor', '/monitor')
    config.add_route('monitor_data', '/monitor_data')

    config.add_route('roll_mon', '/roll_mon')
    config.add_route('roll_mon_data', '/roll_mon_data')

#    config.add_route('all', '/all')
    config.scan()

    # only for advanced example
    json_renderer = JSON()
    json_renderer.add_adapter(date, date_adapter)
    config.add_renderer('json_with_dates', json_renderer)

    return config.make_wsgi_app()
