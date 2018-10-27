from datetime import datetime, timedelta

import jwt
from flask import request, current_app as app, make_response, \
    Blueprint
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


def get_token():
    """Retrieves the JWT contained in the header of the request"""

    try:
        token = request.headers.get('token', None)
        if not token:
            return {
                'iss': "",
                'sub': "",
                'role': "",
                'exp': ""
            }
        return jwt.decode(token, get_secret_key())
    except DecodeError:
        abort(message='Malformed token', code=401)
    except ExpiredSignatureError:
        abort(message='Expired token', code=401)


def generate_jwt_token(username, token_ttl=3600):
    """Generates a JWT"""
    expiration_time = datetime.utcnow() + timedelta(seconds=token_ttl)
    return jwt.encode({
        'iss': "ioet",
        'sub': username,
        'role': "admin",
        'exp': expiration_time
    }, get_secret_key())


@ns.route('/login')
def login():
    auth = request.authorization
    if auth and auth.password == app.config.get("USER_PASSWORD", ""):
        token_ttl = app.config.get('TOKEN_TTL', 3600)
        token = generate_jwt_token(auth.username, token_ttl)
        return jsonify({'token': token.decode('UTF-8')})

    return make_response('Could not verify!', 401, {
        'WWW-Authenticate': 'Basic realm="Login required"'
    })


@ns.route('/logout')
def logout():
    """End the current user session"""
    return "Your session is closed", 401
