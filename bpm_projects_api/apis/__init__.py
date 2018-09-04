"""
Using recommended patterns of scaling from https://flask-restplus.readthedocs.io/en/stable/scaling.html
"""
from .. import config

from flask_restplus import Api
from . import project

api = Api(
    title='BPM Projects API',
    version='0.0.1',
    description='API for managing projects on the IOET BPM'
)

api.add_namespace(project.ns)


@api.errorhandler
def default_error_handler(e):
    if not config.FLASK_DEBUG:
        return {'message': 'An unhandled exception occurred.'}, 500

