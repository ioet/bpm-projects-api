from flask import json
from bpm_projects_api.apis.project import dao as projects_dao
from tests.utils import create_sample_project, create_sample_inactive_project


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
