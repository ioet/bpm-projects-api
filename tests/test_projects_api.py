

def test_index(client):
    client.get('/')
    response = client.get('/')
    assert b"BPM Projects API" in response.data