from flask import json

from bpm_projects_api.apis.project import project_dao
from tests.utils import create_sample_project


def test_search_nothing(client, auth_token):
    """Searching for nothing should return 400"""
    # Given
    search_criteria = {}

    # When
    response = client.post("/projects/search/",
                           headers={'token': auth_token},
                           json=search_criteria, follow_redirects=True)

    # Then
    assert 400 == response.status_code


def test_search_existing_string(client, auth_token, sample_project):
    """Searching for an existing string should return 200"""
    # Given
    assert sample_project
    search_criteria = {'search_string': 'Pro'}

    # When
    response = client.post("/projects/search/",
                           headers={'token': auth_token},
                           json=search_criteria, follow_redirects=True)

    # Then
    assert 200 == response.status_code


def test_search_not_existing_string(client, auth_token):
    """Searching for a not existing string should return 404"""

    search_criteria = {
        'search_string': 'asdf'
    }

    project = create_sample_project()
    client.post("/projects/", headers={'token': auth_token},
                json=project, follow_redirects=True)

    response = client.post("/projects/search/",
                           headers={'token': auth_token},
                           json=search_criteria, follow_redirects=True)

    last_created_project_id = str(project_dao.counter)
    client.delete("/projects/" + last_created_project_id,
                  headers={'token': auth_token},
                  follow_redirects=True)

    assert 404 == response.status_code


def test_search_active_existing(client, auth_token):
    """Searching for an existing active project should return 200"""

    search_criteria = {
        'active': True
    }

    project = create_sample_project()
    client.post("/projects/", headers={'token': auth_token},
                json=project, follow_redirects=True)

    response = client.post("/projects/search/",
                           headers={'token': auth_token},
                           json=search_criteria, follow_redirects=True)

    last_created_project_id = str(project_dao.counter)
    client.delete("/projects/" + last_created_project_id,
                  headers={'token': auth_token},
                  follow_redirects=True)

    assert 200 == response.status_code


def test_search_active_not_existing(client, auth_token):
    """Searching for a not existing active project should return 404"""

    search_criteria = {
        'active': True
    }

    response = client.post("/projects/search/",
                           headers={'token': auth_token},
                           json=search_criteria, follow_redirects=True)

    assert 404 == response.status_code


def test_search_inactive_existing(client, auth_token, sample_project):
    """Searching for an existing inactive project should return 200"""
    # Given
    project_id = sample_project["uid"];
    project_dao.update(project_id, {"active": False})
    search_criteria = {'active': False}

    # When
    response = client.post("/projects/search/",
                           headers={'token': auth_token},
                           json=search_criteria, follow_redirects=True)

    # Then
    assert json.loads(response.data)[0]['uid'] == project_id
    assert 200 == response.status_code


def test_search_inactive_not_exising(client, auth_token):
    """Searching for an inactive not existing project should return 404"""
    search_criteria = {
        'active': False
    }

    response = client.post("/projects/search/{change_status}",
                           headers={'token': auth_token},
                           json=search_criteria, follow_redirects=True)

    assert 404 == response.status_code


def test_search_string_active_existing(client, auth_token):
    """Searching with a string for an active, existing project
    should return 200"""
    search_criteria = {
        'search_string': 'Pro',
        'active': True
    }

    project = create_sample_project()
    client.post("/projects/", headers={'token': auth_token},
                json=project, follow_redirects=True)

    response = client.post("/projects/search/",
                           headers={'token': auth_token},
                           json=search_criteria, follow_redirects=True)

    last_created_project_id = str(project_dao.counter)
    client.delete("/projects/" + last_created_project_id,
                  headers={'token': auth_token},
                  follow_redirects=True)

    assert 200 == response.status_code


def test_search_string_active_not_existing(client, auth_token):
    """Searching with a string for an active, not existing project
    should return 404"""
    search_criteria = {
        'search_string': 'Pro',
        'active': True
    }

    response = client.post("/projects/search/",
                           headers={'token': auth_token},
                           json=search_criteria, follow_redirects=True)

    assert 404 == response.status_code


def test_search_string_inactive_existing(client, auth_token, sample_project):
    """Given a valid search_string and active filter, it should return 200"""
    # Given
    search_criteria = {
        'search_string': 'Pro',
        'active': False
    }
    project_id = sample_project["uid"];
    project_dao.update(project_id, {"active": False})

    # When
    response = client.post("/projects/search/",
                           headers={'token': auth_token},
                           json=search_criteria, follow_redirects=True)

    # Then
    assert json.loads(response.data)[0]['uid'] == project_id
    assert 200 == response.status_code


def test_search_string_inactive_not_existing(client, auth_token):
    """Searching with a string for an inactive, not existing project
    should return 404"""

    search_criteria = {
        'search_string': 'Pro',
        'active': False
    }

    response = client.post("/projects/search/",
                           headers={'token': auth_token},
                           json=search_criteria, follow_redirects=True)

    assert 404 == response.status_code
