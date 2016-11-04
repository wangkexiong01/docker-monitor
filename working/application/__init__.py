# -*- coding: utf-8 -*-

import logging
from logging import Logger

from flask import Flask, Blueprint

from flask.ext.themes2 import Themes

from . import views
from .extensions import db, mail
from .jobs import daemonlized_jobs


def create_app(app_name, config):
    app = Flask(app_name, instance_relative_config=True)
    app.config.from_object('application.settings')
    app.config.from_pyfile(config, silent=True)

    configure_logging(app)
    configure_extensions(app)
    configure_dispatch(app)

    configure_tasks(app)

    configure_context_processors(app)

    return app


def configure_logging(app):
    if app.config.get('DEBUG_LOGGER') != '':
        """
        Always show log level INFO and above
        Use flask env DEBUG to control if generate DEBUG level log

        As for format and log destination, use configuration file to control that
        """

        class DebugLogger(Logger):
            def getEffectiveLevel(self):
                if app.debug:
                    return logging.DEBUG
                else:
                    return Logger.getEffectiveLevel(self)

        app.logger.__class__ = DebugLogger
        app.logger.level = logging.INFO

        debug_handlers = logging.getLogger(app.config['DEBUG_LOGGER']).handlers

        if debug_handlers:
            app.logger.handlers = debug_handlers


def configure_extensions(app):
    db.init_app(app)
    mail.init_app(app)
    Themes(app, app_identifier='monitor')


def configure_dispatch(app):
    for name, cls in views.__dict__.items():
        if isinstance(cls, Blueprint):
            url_prefix = '/' + name if name != 'root' else '/'
            app.register_blueprint(cls, url_prefix=url_prefix)


def configure_tasks(app):
    if not hasattr(app, 'extensions'):
        app.extensions = {}

    app.extensions['job_thread'] = daemonlized_jobs(app)


def configure_context_processors(app):
    pass
