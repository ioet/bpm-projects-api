from flask import Flask
from werkzeug.contrib.fixers import ProxyFix

from bpm_projects_api.apis import api
from bpm_projects_api.core import security


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.wsgi_app = ProxyFix(app.wsgi_app)

    # Configuration located in the folder `instance`
    app.config.from_pyfile('config.py', silent=True)

    api.init_app(app)

    # Security related routes
    app.register_blueprint(security.ns)

    return app
