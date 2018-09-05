from datetime import datetime, timedelta
from functools import wraps

import jwt
from flask import request, current_app as app, make_response, Blueprint
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


def token_required(f):
    @wraps(f)
    def validate_token(*args, **kwargs):
        token = request.headers.get('token', None)
        if not token:
            return abort(message="Token is missing", code=401)

        try:
            data = jwt.decode(token, get_secret_key())
        except DecodeError:
            return abort(message='Then token has an invalid format', code=401)
        except ExpiredSignatureError:
            return abort(message='Expired token', code=401)

        return f(*args, **kwargs)

    return validate_token


@ns.route('/login')
def login():
    auth = request.authorization

    if auth and auth.password == 'secret':
        # Generates a JWToken
        expiration_time = datetime.utcnow() + timedelta(seconds=20)
        token = jwt.encode({
            'user': auth.username,
            'exp': expiration_time,
            'admin': True
        }, get_secret_key())
        return jsonify({'token': token.decode('UTF-8')})

    return make_response('Could not verify!', 401, {
        'WWW-Authenticate': 'Basic realm="Login required"'
    })
