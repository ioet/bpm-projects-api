"""
Using recommended patterns of scaling from
https://flask-restplus.readthedocs.io/en/stable/scaling.html
"""
import flask_opa
from flask import current_app as app
from flask_restplus import Api
from pymongo.errors import DuplicateKeyError

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


@api.errorhandler(DuplicateKeyError)
def handle_duplicated_elements_exceptions(e):
    """Return a 400 status code error"""
    return {'message': "This element already exist in the system"}, 400


@api.errorhandler(flask_opa.OPAException)
def handle_opa_exception(e):
    """Return a 403 due to OPA error"""
    return {'message': str(e)}, 403


@api.errorhandler
def default_error_handler(e):
    if not app.config.get("FLASK_DEBUG", False):
        app.logger.error(e)
        return {'message': 'An unhandled exception occurred.'}, 500


__all__ = [api]
