"""
Global fixtures
"""
import pytest
from bpm_projects_api import create_app


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    yield create_app({"TESTING": True})


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()
