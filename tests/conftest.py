"""
Global fixtures
"""
from importlib import reload

import pytest
from flask import json

from bpm_projects_api import create_app
from tests.utils import url_for, create_sample_project

CONFIGURATIONS = ['TestConfig', 'TestLocalMongoDBConfig', 'TestAzureConfig']

TEST_USER = {
    "name": "testuser@domain.com",
    "password": "secret"
}


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password


@pytest.fixture(scope='session', params=CONFIGURATIONS)
def app(request):
    """Create and configure a new app instance for each test."""
    app = create_app("bpm_projects_api.config.%s" % request.param)

    reload_modules_of_interest(app)

    return app


def reload_modules_of_interest(app):
    """In python 3 modules retain its import state
     so they must be reloaded in order to get the new instances"""
    import bpm_projects_api.apis
    reload(bpm_projects_api.apis)

    import bpm_projects_api.apis.project
    reload(bpm_projects_api.apis.project)

    from bpm_projects_api.model import init_db
    init_db(app)


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


@pytest.yield_fixture
def project_dao():
    from bpm_projects_api.model import project_dao
    yield project_dao
    project_dao.flush()


@pytest.fixture
def sample_project(project_dao):
    return project_dao.create(create_sample_project("0001"))


@pytest.fixture
def another_project(project_dao):
    return project_dao.create(create_sample_project("0002"))
