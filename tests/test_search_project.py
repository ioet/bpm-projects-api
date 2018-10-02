from bpm_projects_api.apis.project import dao as projects_dao
from tests.utils import create_sample_project, create_sample_inactive_project


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

    last_created_project_id = str(projects_dao.counter)
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


def test_search_string_inactive_existing(client, auth_token):
    """Searching with a string for an inactive, existing project
    should return 200"""

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