from flask import json

from tests.utils import create_sample_project


def test_list_all_projects_should_return_nothing(client):
    """Check if all projects are listed"""

    response = client.get("/projects/",
                          follow_redirects=True)
    assert 200 == response.status_code

    json_data = json.loads(response.data)
    assert [] == json_data


def test_post_new_project(client, project_dao):
    """When a new valid project is posted it should be created"""
    # Given
    project = create_sample_project()

    # When
    response = client.post("/projects/",
                           json=project, follow_redirects=True)
    response_json = json.loads(response.data)

    # Then
    assert 201 == response.status_code
    all_entries = project_dao.get_all()
    assert 1 == len(all_entries)


def test_get_all_projects_should_return_a_project(client, sample_project,
                                                  project_dao):
    """Check if the project previously created is there"""
    # When
    response = client.get("/projects/",
                          follow_redirects=True)

    # Then
    assert 200 == response.status_code
    all_entries = project_dao.get_all()
    assert 1 == len(all_entries)


def test_get_valid_project(client,  sample_project):
    """If a valid project id is given it should be returned"""
    # Given
    project_id = sample_project['uid']

    # When
    response = client.get("/projects/%s" % project_id,
                          follow_redirects=True)

    # Then
    assert 200 == response.status_code

    obtained_project = json.loads(response.data)
    assert obtained_project['uid'] == project_id


def test_get_invalid_project(client):
    """If invalid project id is given is should return not found"""

    response = client.get("/projects/xyz",
                          follow_redirects=True)

    assert 404 == response.status_code


def test_delete_existing_project(client, sample_project, project_dao):
    """Delete an existing project should return no content"""
    # Given
    project_id = sample_project['uid']

    # When
    response = client.delete("/projects/%s" % project_id,
                             follow_redirects=True)

    # Then
    assert 204 == response.status_code
    existing_projects = project_dao.get_all()
    assert 0 == len(existing_projects)


def test_get_project_by_name(client, sample_project, project_dao):
    # Given
    project_name = sample_project['short_name']

    # When
    response = client.get("/projects/?name=%s" % project_name,
                          follow_redirects=True)

    # Then
    assert 200 == response.status_code
    obtained_project = json.loads(response.data)
    assert project_name in obtained_project[0]['comments'] or \
        project_name in obtained_project[0]['short_name']


def test_get_project_is_active(client, sample_project, project_dao):
    # Given
    project_state = sample_project['active']

    # When
    response = client.get("/projects/?active=%s" % project_state,
                          follow_redirects=True)
    # Then
    assert 200 == response.status_code
    obtained_project = json.loads(response.data)
    assert obtained_project[0]['active'] is True


def test_get_project_name_is_active(client, sample_project, project_dao):
    # Given
    project_state = sample_project['active']
    project_name = sample_project['short_name']

    # When
    response = client.get("/projects/?name={}&active={}".format(project_name,
                          project_state), follow_redirects=True)

    # Then
    assert 200 == response.status_code
    obtained_project = json.loads(response.data)
    assert obtained_project[0]['active'] is True and\
        obtained_project[0]['short_name'] == project_name


def test_get_project_name_is_inactive(client, sample_project, project_dao):
    # Given
    project_state = sample_project['active']
    project_name = sample_project['short_name']

    # When
    response = client.get("/projects/?name={}&active={}".format(project_name,
                          project_state), follow_redirects=True)

    # Then
    assert 200 == response.status_code
    obtained_project = json.loads(response.data)
    assert not obtained_project[0]['active'] is not True and\
        obtained_project[0]['short_name'] == project_name
