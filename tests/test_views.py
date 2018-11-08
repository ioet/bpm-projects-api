from tests.utils import url_for


def test_index_page_is_ok(client):
    """ Is home page present """

    response = client.get('/')
    assert response.status_code == 200
    assert b"BPM Projects API" in response.data
