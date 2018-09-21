from flask import json
from bpm_projects_api.apis.project import dao as projects_dao
from tests.utils import create_sample_project, create_sample_inactive_project


def test_list_all_projects_should_return_nothing(client, auth_token):
    """Check if all projects are listed"""

    response = client.get("/projects/", headers={'token': auth_token}, follow_redirects=True)
    assert 200 == response.status_code

    json_data = json.loads(response.data)
    assert json_data == []


def test_post_new_project(client, auth_token):
    """When a new valid project is posted it should be created"""

    project = create_sample_project()
    response = client.post("/projects/", headers={'token': auth_token},
                           json=project, follow_redirects=True)

    last_created_project_id = str(projects_dao.counter)
    client.delete("/projects/" + last_created_project_id,
                  headers={'token': auth_token},
                  follow_redirects=True)

    assert 201 == response.status_code

    created_project = json.loads(response.data)
    assert created_project['uid']


def test_get_all_projects_should_return_a_project(client, auth_token):
    """Check if the project previously created is there"""

    project = create_sample_project()
    client.post("/projects/", headers={'token': auth_token},
                json=project, follow_redirects=True)

    response = client.get("/projects/", headers={'token': auth_token}, follow_redirects=True)

    last_created_project_id = str(projects_dao.counter)
    client.delete("/projects/" + last_created_project_id,
                  headers={'token': auth_token},
                  follow_redirects=True)

    assert 200 == response.status_code

    json_data = json.loads(response.data)
    assert len(json_data) == 1


def test_get_valid_project(client, auth_token):
    """If a valid project id is given it should be returned"""

    project = create_sample_project()
    client.post("/projects/", headers={'token': auth_token},
                json=project, follow_redirects=True)

    last_created_project_id = str(projects_dao.counter)
    response = client.get("/projects/" + last_created_project_id,
                          headers={'token': auth_token},
                          follow_redirects=True)

    last_created_project_id = str(projects_dao.counter)
    client.delete("/projects/" + last_created_project_id,
                  headers={'token': auth_token},
                  follow_redirects=True)

    assert 200 == response.status_code

    obtained_project = json.loads(response.data)
    assert obtained_project['uid'] == last_created_project_id


def test_get_invalid_project(client, auth_token):
    """If invalid project id is given is should return not found"""

    response = client.get("/projects/xyz", headers={'token': auth_token}, follow_redirects=True)

    assert 404 == response.status_code


def test_put_project_properties(client, auth_token):
    """Put should only update given properties"""

    project = create_sample_project()
    client.post("/projects/", headers={'token': auth_token},
                json=project, follow_redirects=True)

    last_created_project_id = str(projects_dao.counter)
    new_name = "Updated project" + last_created_project_id
    properties_update = {
        "short_name": new_name,
        "properties_table": [
            {
                "id": "company",
                "content": "ACME"
            }
        ],
        "active": True
    }

    response = client.patch("/projects/" + last_created_project_id,
                          json=properties_update,
                          headers={'token': auth_token},
                          follow_redirects=True)

    client.delete("/projects/" + last_created_project_id,
                  headers={'token': auth_token},
                  follow_redirects=True)

    assert 200 == response.status_code

    obtained_project = json.loads(response.data)
    assert obtained_project['short_name'] == new_name
    assert len(obtained_project["properties_table"]) == 1  # Substituted, not added


def test_delete_existing_project(client, auth_token):
    """Delete an existing project should return no content"""

    project = create_sample_project()
    client.post("/projects/", headers={'token': auth_token},
                json=project, follow_redirects=True)

    # Given
    assert len(projects_dao.projects) == 1

    # When
    last_created_project_id = str(projects_dao.counter)
    response = client.delete("/projects/" + last_created_project_id,
                             headers={'token': auth_token},
                             follow_redirects=True)

    # Then
    assert 204 == response.status_code
    assert 0 == len(response.data)
    
    assert len(projects_dao.projects) == 0


def test_search_nothing(client, auth_token):
    """Searching for nothing should return 404"""

    search_criteria = {

    }

    response = client.post("/projects/search/",
                           headers={'token': auth_token},
                           json=search_criteria, follow_redirects=True)

    assert 404 == response.status_code


def test_search_existing_string(client, auth_token):
    """Searching for an existing string should return 200"""

    search_criteria = {
        'search_string': 'Pro'
    }

    project = create_sample_project()
    client.post("/projects/", headers={'token': auth_token},
                json=project, follow_redirects=True)

    response = client.post("/projects/search/",
                           headers={'token': auth_token},
                           json=search_criteria, follow_redirects=True)

    last_created_project_id = str(projects_dao.counter)
    client.delete("/projects/" + last_created_project_id,
                  headers={'token': auth_token},
                  follow_redirects=True)

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

    last_created_project_id = str(projects_dao.counter)
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

    last_created_project_id = str(projects_dao.counter)
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


def test_search_inactive_existing(client, auth_token):
    """Searching for an existing inactive project should return 200"""

    search_criteria = {
        'active': False
    }

    project = create_sample_inactive_project()
    client.post("/projects/", headers={'token': auth_token},
                json=project, follow_redirects=True)

    response = client.post("/projects/search/",
                           headers={'token': auth_token},
                           json=search_criteria, follow_redirects=True)

    last_created_project_id = str(projects_dao.counter)
    client.delete("/projects/" + last_created_project_id,
                  headers={'token': auth_token},
                  follow_redirects=True)

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
    """Searching with a string for an active, existing project should return 200"""

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

    last_created_project_id = str(projects_dao.counter)
    client.delete("/projects/" + last_created_project_id,
                  headers={'token': auth_token},
                  follow_redirects=True)

    assert 200 == response.status_code


def test_search_string_active_not_existing(client, auth_token):
    """Searching with a string for an active, not existing project should return 404"""

    search_criteria = {
        'search_string': 'Pro',
        'active': True
    }

    response = client.post("/projects/search/",
                           headers={'token': auth_token},
                           json=search_criteria, follow_redirects=True)

    assert 404 == response.status_code


def test_search_string_inactive_existing(client, auth_token):
    """Searching with a string for an inactive, existing project should return 200"""

    search_criteria = {
        'search_string': 'Pro',
        'active': False
    }

    project = create_sample_inactive_project()
    client.post("/projects/", headers={'token': auth_token},
                json=project, follow_redirects=True)

    response = client.post("/projects/search/",
                           headers={'token': auth_token},
                           json=search_criteria, follow_redirects=True)

    last_created_project_id = str(projects_dao.counter)
    client.delete("/projects/" + last_created_project_id,
                  headers={'token': auth_token},
                  follow_redirects=True)

    assert 200 == response.status_code


def test_search_string_inactive_not_existing(client, auth_token):
    """Searching with a string for an inactive, not existing project should return 404"""

    search_criteria = {
        'search_string': 'Pro',
        'active': False
    }

    response = client.post("/projects/search/",
                           headers={'token': auth_token},
                           json=search_criteria, follow_redirects=True)

    assert 404 == response.status_code


def test_activate_active(client, auth_token):
    """Activating an active project returns 404"""

    project = create_sample_project()
    client.post("/projects/", headers={'token': auth_token},
                json=project, follow_redirects=True)

    last_created_project_id = str(projects_dao.counter)

    response = client.patch("/projects/status/activate/" + last_created_project_id,
                           headers={'token': auth_token},
                           follow_redirects=True)

    client.delete("/projects/" + last_created_project_id,
                  headers={'token': auth_token},
                  follow_redirects=True)

    assert 404 == response.status_code


def test_activate_inactive(client, auth_token):
    """Activating an inactive project sets active to True, returns 200"""

    project = create_sample_inactive_project()
    client.post("/projects/", headers={'token': auth_token},
                json=project, follow_redirects=True)

    last_created_project_id = str(projects_dao.counter)

    response = client.patch("/projects/status/activate/" + last_created_project_id,
                           headers={'token': auth_token},
                           follow_redirects=True)

    client.delete("/projects/" + last_created_project_id,
                  headers={'token': auth_token},
                  follow_redirects=True)

    returned_project = json.loads(response.data)
    assert returned_project['active'] is True
    assert 200 == response.status_code


def test_deactivating_inactive(client, auth_token):
    """Deactivating an inactive project returns 404"""

    project = create_sample_inactive_project()
    client.post("/projects/", headers={'token': auth_token},
                json=project, follow_redirects=True)

    last_created_project_id = str(projects_dao.counter)

    response = client.patch("/projects/status/deactivate/" + last_created_project_id,
                           headers={'token': auth_token},
                           follow_redirects=True)

    client.delete("/projects/" + last_created_project_id,
                  headers={'token': auth_token},
                  follow_redirects=True)

    assert 404 == response.status_code


def test_deactivating_active(client, auth_token):
    """Deactivating an active projects sets active to False, returns 200"""

    project = create_sample_project()
    client.post("/projects/", headers={'token': auth_token},
                json=project, follow_redirects=True)

    last_created_project_id = str(projects_dao.counter)

    response = client.patch("/projects/status/deactivate/" + last_created_project_id,
                           headers={'token': auth_token},
                           follow_redirects=True)

    client.delete("/projects/" + last_created_project_id,
                  headers={'token': auth_token},
                  follow_redirects=True)

    returned_project = json.loads(response.data)
    assert returned_project['active'] is False
    assert 200 == response.status_code


def test_deactivate_not_existing(client, auth_token):
    """Deactivating a not existing project returns 404"""

    last_created_project_id = str(projects_dao.counter)

    response = client.patch("/projects/status/deactivate/" + last_created_project_id,
                           headers={'token': auth_token},
                           follow_redirects=True)
    print(response)

    assert 404 == response.status_code


def test_activate_not_existing(client, auth_token):
    """Activating a not existing project returns 404"""

    last_created_project_id = str(projects_dao.counter)

    response = client.patch("/projects/status/activate/" + last_created_project_id,
                           headers={'token': auth_token},
                           follow_redirects=True)

    assert 404 == response.status_code