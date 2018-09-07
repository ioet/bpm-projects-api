import jwt
from flask import json


def test_successful_login_returns_valid_jwt(auth, user, secret_token_key):
    """ Given valid auth credentials when login then returns valid JWT"""
    response = auth.login(user.username, user.password)

    json_data = json.loads(response.data)
    assert "token" in json_data

    jwt_payload = jwt.decode(json_data["token"], secret_token_key)
    assert jwt_payload["sub"] == user.username


def test_invalid_login_returns_401(auth, user):
    """ Given invalid auth credentials return 401 """
    response = auth.login(user.username, user.password + "invalidatorcontent")
    assert response.status_code == 401


def test_successful_logout(auth, user):
    """After logout a user_id should not exist in the session"""
    auth.login(user.username, user.password)
    response = auth.logout()
    assert response.status_code == 200


def test_logout_unexisting_session(auth):
    """If logout is called when no session exists the response should be Ok"""
    resp1 = auth.logout()
    resp2 = auth.logout()
    assert resp1.status_code == resp2.status_code == 200
