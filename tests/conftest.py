"""
Global fixtures
"""
import pytest
from bpm_projects_api import create_app


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    return create_app({
        "TESTING": True,
        "SECRET_KEY": "secretkeyfordevelopment",
        "USER_PASSWORD": "secret",
        "SERVER_NAME": "localhost"
    })


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def user(app):
    """A test user"""
    class User:
        def __init__(self, username, password):
            self.username = username
            self.password = password

    return User("testuser@ioet.com", app.config["USER_PASSWORD"])


@pytest.fixture
def secret_token_key(app):
    """A secret key to sign JWTs"""
    return app.config["SECRET_KEY"]


@pytest.fixture
def sample_project():
    """A project instance used for end-to-end tests"""
    pass
