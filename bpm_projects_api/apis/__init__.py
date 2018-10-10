"""
Using recommended patterns of scaling from
https://flask-restplus.readthedocs.io/en/stable/scaling.html
"""
from flask import current_app as app
from flask_restplus import Api

from bpm_projects_api.model.errors \
    import MissingResource, InvalidMatch, InvalidInput
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


@api.errorhandler(MissingResource)
def handle_not_found_exceptions(e):
    """Return a 404 status code error"""
    return {'message': str(e)}, 404


@api.errorhandler(InvalidMatch)
def handle_no_match_exceptions(e):
    """Return a 204 status code error"""
    return {'message': str(e)}, 204


@api.errorhandler(InvalidInput)
def handle_invalid_request_exceptions(e):
    """Return a 400 status code error"""
    return {'message': str(e)}, 400


@api.errorhandler
def default_error_handler(e):
    if "FLASK_DEBUG" not in app.config:
        app.logger.error(e)
        return {'message': 'An unhandled exception occurred.'}, 500


__all__ = [api]
