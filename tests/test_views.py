def test_index_page_is_ok(client):
    """ Is home page present """

    response = client.get('/')
    assert response.status_code == 200
    assert b"BPM Projects API" in response.data


def test_login_page_requires_authentication(client):
    """ Is login page present and requires authentication """

    response = client.get('/login')
    assert response.status_code == 401
