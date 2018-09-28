"""
Global fixtures
"""
import pytest
from flask import json

from bpm_projects_api import create_app
from tests.utils import url_for, open_with_basic_auth

test_config = {
    "TESTING": True,
    "SECRET_KEY": "secretkeyfordevelopment",
    "USER_PASSWORD": "secret",
    "SERVER_NAME": "localhost",
    "TEST_USER": "testuser@domain.com"
}


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password


class AuthActions:
    """Auth actions container in tests"""

    def __init__(self, app, client):
        self._app = app
        self._client = client

    def login(self, username=test_config["TEST_USER"],
              password=test_config["USER_PASSWORD"]):
        login_url = url_for("security.login", self._app)
        return open_with_basic_auth(self._client,
                                    login_url,
                                    username,
                                    password)

    def logout(self):
        return self._client.get(url_for("security.logout",
                                        self._app), follow_redirects=True)


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    return create_app(config=test_config,
                      config_object='bpm_projects_api.config.TestingConfig')



@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def user(app):
    """A test user"""
    return User(test_config["TEST_USER"], app.config["USER_PASSWORD"])


@pytest.fixture
def api():
    """Projects API"""
    from bpm_projects_api.apis import api
    return api


@pytest.fixture
def secret_token_key(app):
    """A secret key to sign JWTs"""
    return app.config["SECRET_KEY"]


@pytest.fixture
def auth(app, client):
    return AuthActions(app, client)


@pytest.fixture
def auth_token(auth, user):
    response = auth.login(user.username, user.password)
    return json.loads(response.data)["token"]
