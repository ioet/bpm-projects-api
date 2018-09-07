import jwt
from flask import json

from tests.utils import open_with_basic_auth


def test_successful_login_returns_valid_jwt(client, user, secret_token_key):
    """ Given valid auth credentials when login then returns valid JWT"""
    response = open_with_basic_auth(
        client, "/login", user.username, user.password
    )
    json_data = json.loads(response.data)

    assert "token" in json_data

    jwt_payload = jwt.decode(json_data["token"], secret_token_key)
    assert jwt_payload["sub"] == user.username


def test_invalid_login_returns_401(client, user):
    """ Given invalid auth crendentials return 401 """
    response = open_with_basic_auth(
        client, "/login", user.username, user.password + "extra"
    )

    assert response.status_code == 401
