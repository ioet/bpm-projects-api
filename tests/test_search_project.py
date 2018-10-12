from flask import json

from tests.utils import create_sample_project


def test_search_nothing(client, auth_token):
    """Searching for nothing should return 400"""
    # Given
    search_criteria = {}

    # When
    response = client.get("/projects/search/",
                           headers={'token': auth_token},
                           json=search_criteria,
                           follow_redirects=True)

    # Then
    assert 400 == response.status_code


def test_search_existing_string(client, auth_token, sample_project):
    """Searching for an existing string should return 200"""
    # Given
    assert sample_project
    # When
    response = client.get("/projects/search/?search_string=Project",
                           headers={'token': auth_token},
                           follow_redirects=True)

    # Then
    assert 200 == response.status_code
    assert json.loads(response.data)[0]['uid'] == sample_project['uid']


def test_search_non_existing_string(client, auth_token, sample_project):
    """Searching for a not existing string should return 204"""
    # Given
    search_criteria = {'search_string': 'non matching test'}

    # When
    response = client.get("/projects/search/",
                           headers={'token': auth_token},
                           json=search_criteria, follow_redirects=True)

    # Then
    assert 204 == response.status_code


def test_search_active_existing(client, auth_token, sample_project):
    """Searching for an existing active project should return 200"""
    # Given
    search_criteria = {
        'active': True
    }

    # When
    response = client.get("/projects/search/?active=true",
                           headers={'token': auth_token},
                           follow_redirects=True)

    # Then
    assert json.loads(response.data)[0]['uid'] == sample_project['uid']
    assert 200 == response.status_code


def test_search_active_non_existing(client, auth_token):
    """Searching for a not existing active project should return 204"""

    search_criteria = {
        'active': True
    }

    response = client.get("/projects/search/",
                           headers={'token': auth_token},
                           json=search_criteria, follow_redirects=True)

    assert 204 == response.status_code


def test_search_existing_inactive(client, auth_token, sample_project, another_project, project_dao):
    """Searching for an existing inactive project should return 200"""
    # Given
    inactive_project_id = another_project["uid"];
    project_dao.update(inactive_project_id, {"active": False})

    search_criteria = {'active': False}

    # When
    response = client.get("/projects/search/",
                           headers={'token': auth_token},
                           json=search_criteria, follow_redirects=True)

    # Then
    response_json = json.loads(response.data)
    assert 1 == len(response_json)
    assert response_json[0]['uid'] == inactive_project_id
    assert 200 == response.status_code


def test_search_non_existing_inactive(client, auth_token):
    """Searching for an inactive not existing project should return 404"""
    search_criteria = {
        'active': False
    }

    response = client.post("/projects/search/{change_status}",
                           headers={'token': auth_token},
                           json=search_criteria, follow_redirects=True)

    assert 404 == response.status_code


def test_search_string_existing_active(client, auth_token, sample_project):
    """Searching with a string for an active, existing project
    should return 200"""
    # Given
    search_criteria = {
        'search_string': 'Project',
        'active': True
    }

    # When
    response = client.get("/projects/search/",
                           headers={'token': auth_token},
                           json=search_criteria, follow_redirects=True)

    # Then
    assert json.loads(response.data)[0]['uid'] == sample_project['uid']
    assert 200 == response.status_code


def test_search_string_non_existing_active(client, auth_token):
    """Searching with a string for an active, not existing project
    should return 204"""
    search_criteria = {
        'search_string': 'Pro',
        'active': True
    }

    response = client.get("/projects/search/",
                           headers={'token': auth_token},
                           json=search_criteria, follow_redirects=True)

    assert 204 == response.status_code


def test_search_string_inactive_existing(client, auth_token, sample_project, project_dao):
    """Given a valid search_string and active filter, it should return 200"""
    # Given
    search_criteria = {
        'search_string': 'Project',
        'active': False
    }
    project_id = sample_project["uid"];
    project_dao.update(project_id, {"active": False})

    # When
    response = client.get("/projects/search/",
                           headers={'token': auth_token},
                           json=search_criteria, follow_redirects=True)

    # Then
    assert json.loads(response.data)[0]['uid'] == project_id
    assert 200 == response.status_code


def test_search_string_non_existing_inactive(client, auth_token):
    """Searching with a string for an inactive, not existing project
    should return 204"""

    search_criteria = {
        'search_string': 'Pro',
        'active': False
    }

    response = client.get("/projects/search/",
                           headers={'token': auth_token},
                           json=search_criteria, follow_redirects=True)

    assert 204 == response.status_code
