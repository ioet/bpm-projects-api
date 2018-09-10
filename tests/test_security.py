import jwt
from flask import json


def test_successful_login_returns_valid_jwt(auth, user, secret_token_key):
    """ Given valid auth credentials when login then returns valid JWT"""
    response = auth.login()

    json_data = json.loads(response.data)
    assert "token" in json_data

    jwt_payload = jwt.decode(json_data["token"], secret_token_key)
    assert jwt_payload["sub"] == user.username


def test_invalid_login_returns_401(auth, user):
    """ Given invalid auth credentials return 401 """
    response = auth.login(user.username, user.password + "invalidatorcontent")
    assert 401 == response.status_code


def test_successful_logout(auth):
    """After logout a user_id should not exist in the session"""
    auth.login()
    response = auth.logout()
    assert 200 == response.status_code


def test_logout_unexisting_session(auth):
    """If logout is called when no session exists the response should be Ok"""
    resp1 = auth.logout()
    resp2 = auth.logout()
    assert 200 == resp1.status_code == resp2.status_code
