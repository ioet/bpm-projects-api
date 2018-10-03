from flask import json

from tests.utils import create_sample_project


def test_list_all_projects_should_return_nothing(client, auth_token):
    """Check if all projects are listed"""

    response = client.get("/projects/",
                          headers={'token': auth_token},
                          follow_redirects=True)
    assert 200 == response.status_code

    json_data = json.loads(response.data)
    assert [] == json_data


def test_post_new_project(client, auth_token, project_dao):
    """When a new valid project is posted it should be created"""
    # Given
    project = create_sample_project()

    # When
    response = client.post("/projects/", headers={'token': auth_token},
                           json=project, follow_redirects=True)
    response_json = json.loads(response.data)

    # Then
    assert 201 == response.status_code
    all_entries = project_dao.get_all()
    assert 1 == len(all_entries)


def test_get_all_projects_should_return_a_project(client, auth_token, sample_project, project_dao):
    """Check if the project previously created is there"""
    # When
    response = client.get("/projects/",
                          headers={'token': auth_token},
                          follow_redirects=True)

    # Then
    assert 200 == response.status_code
    all_entries = project_dao.get_all()
    assert 1 == len(all_entries)


def test_get_valid_project(client, auth_token, sample_project):
    """If a valid project id is given it should be returned"""
    # Given
    project_id = sample_project['uid']

    # When
    response = client.get("/projects/%s" % project_id,
                          headers={'token': auth_token},
                          follow_redirects=True)

    # Then
    assert 200 == response.status_code

    obtained_project = json.loads(response.data)
    assert obtained_project['uid'] == project_id


def test_get_invalid_project(client, auth_token):
    """If invalid project id is given is should return not found"""

    response = client.get("/projects/xyz",
                          headers={'token': auth_token},
                          follow_redirects=True)

    assert 404 == response.status_code


def test_delete_existing_project(client, auth_token, sample_project, project_dao):
    """Delete an existing project should return no content"""
    # Given
    project_id = sample_project['uid']

    # When
    response = client.delete("/projects/%s" % project_id,
                             headers={'token': auth_token},
                             follow_redirects=True)

    # Then
    assert 204 == response.status_code
    existing_projects = project_dao.get_all()
    assert 0 == len(existing_projects)
