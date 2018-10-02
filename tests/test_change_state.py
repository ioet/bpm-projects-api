from flask import json

from bpm_projects_api.apis.project import dao as projects_dao


def test_activate_inactive(client, auth_token, sample_project):
    """Activating an inactive project sets active to True, returns 204"""
    # Given
    project_id = sample_project["uid"];
    projects_dao.update(project_id, {"active": False})

    # When
    response = client.post("/projects/%s" % project_id,
                           data={'active': True},
                           headers={'token': auth_token},
                           follow_redirects=True)

    # Then
    saved_project = json.loads(client.get("/projects/%s" % project_id).data)
    assert saved_project['active'] is True
    assert 204 == response.status_code


def test_deactivating_active(client, auth_token, sample_project):
    """Deactivating an active projects sets active to False, returns 204"""
    # Given
    project_id = sample_project["uid"];

    # When
    response = client.post("/projects/%s" % project_id,
                           data={'active': False},
                           headers={'token': auth_token},
                           follow_redirects=True)

    # Then
    saved_project = json.loads(client.get("/projects/%s" % project_id).data)
    assert saved_project['active'] is False
    assert 204 == response.status_code


def test_deactivate_not_existing(client, auth_token):
    """Deactivating a not existing project returns 404"""
    # When
    response = client.post("/projects/%s" % 789,
                           data={'active': True},
                           headers={'token': auth_token},
                           follow_redirects=True)

    # Then
    assert 404 == response.status_code


def test_activate_not_existing(client, auth_token):
    """Activating a not existing project returns 404"""
    # When
    response = client.post("/projects/%s" % 789,
                           data={'active': False},
                           headers={'token': auth_token},
                           follow_redirects=True)

    # Then
    assert 404 == response.status_code


def test_empty_request(client, auth_token, sample_project):
    """Given an empty request it should return 400"""
    # Given
    project_id = sample_project["uid"];

    # When
    response = client.post("/projects/%s" % project_id,
                           data={},
                           headers={'token': auth_token},
                           follow_redirects=True)

    # Then
    assert 400 == response.status_code


def test_invalid_request(client, auth_token, sample_project):
    """Given an invalid request it should return 400"""
    # Given
    project_id = sample_project["uid"];

    # When
    response = client.post("/projects/%s" % project_id,
                           data={"invalid_field": "value"},
                           headers={'token': auth_token},
                           follow_redirects=True)

    # Then
    assert 400 == response.status_code
