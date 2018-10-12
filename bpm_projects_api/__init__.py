import os
import sys

from flask import Flask
from werkzeug.contrib.fixers import ProxyFix


def create_app(config_path='bpm_projects_api.config.InMemoryDevelopmentConfig',
               config_data=None):
    """Create and configure an instance of the Flask app."""
    app = Flask(__name__, instance_relative_config=True)

    # Needed when using a wsgi server (mainly for production)
    app.wsgi_app = ProxyFix(app.wsgi_app)

    init_app_config(app, config_path, config_data)

    init_app(app)

    return app


def init_app_config(app, config_path, config_data=None):
    if config_path:
        app.config.from_object(config_path)
    else:
        # ensure the instance folder exists
        try:
            os.makedirs(app.instance_path)
        except OSError:
            pass

        # Located in `/instance`
        app.config.from_pyfile('config.py', silent=True)

    if config_data:
        app.config.update(config_data)


def init_app(app):
    import bpm_projects_api.model as model
    model.init_app(app)

    from bpm_projects_api.apis import api
    api.init_app(app)

    cors_origins = app.config.get('CORS_ORIGINS')
    if cors_origins:
        from flask_cors import CORS
        cors_origins_list = cors_origins.split(",")
        CORS(app, resources={r"/*": {"origins": cors_origins_list}})
        app.logger.info("Allowing CORS access to [%s]" % cors_origins)

    from bpm_projects_api.core import security
    app.register_blueprint(security.ns)  # Security endpoints

    if app.config.get('DEBUG'):
        add_debug_toolbar(app)

    if app.config.get('FLASK_ENV') == 'production':
        sys.stdout = sys.stderr = open('bpm-projects-api.log', 'wt')


def add_debug_toolbar(app):
    app.config['DEBUG_TB_PANELS'] = (
        'flask_debugtoolbar.panels.versions.VersionDebugPanel',
        'flask_debugtoolbar.panels.timer.TimerDebugPanel',
        'flask_debugtoolbar.panels.headers.HeaderDebugPanel',
        'flask_debugtoolbar.panels.request_vars.RequestVarsDebugPanel',
        'flask_debugtoolbar.panels.config_vars.ConfigVarsDebugPanel',
        'flask_debugtoolbar.panels.template.TemplateDebugPanel',
        'flask_debugtoolbar.panels.logger.LoggingPanel',
        'flask_debugtoolbar.panels.route_list.RouteListDebugPanel',
        'flask_debugtoolbar.panels.profiler.ProfilerDebugPanel'
    )

    from flask_debugtoolbar import DebugToolbarExtension
    toolbar = DebugToolbarExtension()
    toolbar.init_app(app)
