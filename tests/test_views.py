from utils import url_for


def test_index_page_is_ok(client):
    """ Is home page present """

    response = client.get('/')
    assert response.status_code == 200
    assert b"BPM Projects API" in response.data


def test_login_page_requires_authentication(app, client):
    """ Is login page present and requires authentication """
    response = client.get(url_for('security.login', app))
    assert response.status_code == 401
