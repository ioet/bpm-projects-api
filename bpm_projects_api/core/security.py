from datetime import datetime, timedelta
from functools import wraps

import jwt
from flask import request, current_app as app, make_response, \
    Blueprint, session, redirect
from flask.json import jsonify
from flask_restplus import abort
from jwt import DecodeError, ExpiredSignatureError

ns = Blueprint('security', __name__)

authorizations = {
    'BPM Token': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'token'
    }
}


def get_secret_key():
    """
    Returns the secret key to encode JWTs
    :return: str
    """
    return app.config['SECRET_KEY']


class PolicyError(Exception):
    """
    Errors related to lack of auth credentials on a token payload
    """
    pass


def token_required(f, validate_function=None):
    @wraps(f)
    def validate_token(*args, **kwargs):
        token = request.headers.get('token', None)
        if not token:
            return abort(message="Token is missing", code=401)

        try:
            data = jwt.decode(token, get_secret_key())
            if validate_function is not None:
                validate_function(data)
        except DecodeError:
            return abort(message='Malformed token', code=401)
        except ExpiredSignatureError:
            return abort(message='Expired token', code=401)
        except PolicyError as error:
            return abort(message=error, code=401)

        return f(*args, **kwargs)

    return validate_token


class TokenPolicies(object):
    """
    Security policies checks for tokens
    """

    @staticmethod
    def administrator_required(f):
        """
        Is the user an administrator
        """

        def check_if_user_is_administrator(data):
            if data.get('role', 'user') != 'admin':
                raise PolicyError("Admin user is required")

        return token_required(f,
                              validate_function=check_if_user_is_administrator)


@ns.route('/login')
def login():
    auth = request.authorization

    if auth and auth.password == app.config.get("USER_PASSWORD", ""):
        # Generates a JWToken
        token_ttl = app.config.get('TOKEN_TTL', 3600)
        expiration_time = datetime.utcnow() + timedelta(seconds=token_ttl)
        token = jwt.encode({
            'iss': "ioet.com",
            'sub': auth.username,
            'role': "admin",
            'exp': expiration_time
        }, get_secret_key())
        return jsonify({'token': token.decode('UTF-8')})

    return make_response('Could not verify!', 401, {
        'WWW-Authenticate': 'Basic realm="Login required"'
    })


@ns.route('/logout')
def logout():
    """End the current user session"""
    session.clear()
    return redirect('/')


token_policies = TokenPolicies
