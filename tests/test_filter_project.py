from flask import json
from tests.utils import create_sample_project


def test_filter_nothing_return_all_projects(client, sample_project):
    """Searching for nothing should return 200"""
    # Given
    assert sample_project
    search_criteria = {}

    # When
    response = client.get("/projects/",
                          json=search_criteria,
                          follow_redirects=True)

    # Then
    assert 200 == response.status_code
    assert len(json.loads(response.data)) > 0


def test_filter_shortname_return_project(client, sample_project):
    """Searching by shortname return filtered projects"""
    # Given
    assert sample_project

    # When
    response = client.get("/projects/?short_name=Project")

    # Then
    assert 200 == response.status_code
    assert json.loads(response.data)[0]['uid'] == sample_project['uid']


def test_filter_active_return_projects(client, sample_project):
    """Searching with active filter return true"""

    # Given
    assert sample_project
    search_criteria = {'active': 'true'}

    # When
    response = client.get("/projects/",
                          json=search_criteria,
                          follow_redirects=True)

    # Then
    assert 200 == response.status_code
    assert json.loads(response.data)[0]['active'] is True


def test_filter_active_and_shortname_return_projects(client, sample_project):
    """Searching with active and Shortname return filtered projects"""

    # Given
    assert sample_project
    search_criteria = {'active': 'true'}

    # When
    response = client.get("/projects/",
                          json=search_criteria,
                          follow_redirects=True)

    # Then
    assert 200 == response.status_code
    assert json.loads(response.data)[0]['active'] is True
    assert json.loads(response.data)[0]['uid'] == sample_project['uid']
    assert len(json.loads(response.data)) > 0










