"""
Using recommended patterns of scaling from
https://flask-restplus.readthedocs.io/en/stable/scaling.html
"""
from flask_restplus import Api

from . import project
from ..core import security

api = Api(
    title='BPM Projects API',
    version='0.0.1',
    description='API for managing projects on the IOET BPM',
    authorizations=security.authorizations, security="BPM Token",
    default=project.ns.name, default_label=project.ns.name
)

api.add_namespace(project.ns)


@api.errorhandler
def default_error_handler(e):
    try:
        from instance import config
        if not config.FLASK_DEBUG:
            return {'message': 'An unhandled exception occurred.'}, 500
    except Exception:
        pass
