"""
Global fixtures
"""
from imp import reload

import pytest
from flask import json

from bpm_projects_api import create_app
from tests.utils import url_for, open_with_basic_auth, create_sample_project

CONFIGURATIONS = ['TestConfig', 'TestAzureDevelopmentConfig']

TEST_USER = {
    "name": "testuser@domain.com",
    "password": "secret"
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

    def login(self, username=TEST_USER["name"],
              password=TEST_USER["password"]):
        login_url = url_for("security.login", self._app)
        return open_with_basic_auth(self._client,
                                    login_url,
                                    username,
                                    password)

    def logout(self):
        return self._client.get(url_for("security.logout",
                                        self._app), follow_redirects=True)


@pytest.fixture(scope='session', params=CONFIGURATIONS)
def app(request):
    """Create and configure a new app instance for each test."""
    app = create_app("bpm_projects_api.config.%s" % request.param)

    reload_modules_of_interest()

    return app


def reload_modules_of_interest():
    """In python 3 modules retain its import state
     so they must be reloaded in order to get the new instances"""
    import bpm_projects_api.apis.project
    reload(bpm_projects_api.apis.project)

@pytest.fixture
def client(app):
    """A test client for the app."""
    with app.test_client() as c:
        return c


@pytest.fixture
def user(app):
    """A test user"""
    return User(TEST_USER["name"], TEST_USER["password"])


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


@pytest.yield_fixture
def project_dao():
    from bpm_projects_api.model import project_dao
    yield project_dao
    project_dao.delete()


@pytest.fixture
def sample_project(project_dao):
    return project_dao.create(create_sample_project())
