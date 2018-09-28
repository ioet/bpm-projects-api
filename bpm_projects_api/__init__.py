import os

from flask import Flask
from werkzeug.contrib.fixers import ProxyFix


def create_app(config=None,
               config_object='bpm_projects_api.config.DevelopmentConfig'):
    """Create and configure an instance of the Flask app."""
    app = Flask(__name__, instance_relative_config=True)

    # Needed when using a wsgi server (mainly for production)
    app.wsgi_app = ProxyFix(app.wsgi_app)

    if config_object is not None:
        app.config.from_object(config_object)
    elif config is None:
        # ensure the instance folder exists
        try:
            os.makedirs(app.instance_path)
        except OSError:
            pass

        # Located in `/instance`
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Used mostly for testing
        app.config.update(config)

    from bpm_projects_api.apis import api
    api.init_app(app)

    from bpm_projects_api.core import security
    app.register_blueprint(security.ns)  # Security endpoints

    return app
