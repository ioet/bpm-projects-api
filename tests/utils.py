import base64

import flask


def encodeBase64(str: str):
    """ Encodes a string to base64 """
    return base64.b64encode(str.encode("UTF8")).decode()


def open_with_basic_auth(client, login_url, username, password, method='GET'):
    """ Authenticates in a login_url using Basic Authentication """
    return client.open(login_url,
                       method=method,
                       headers={
                           'Authorization': "Basic %s" % encodeBase64(
                               "{}:{}".format(username, password)
                           )
                       }
                       )


def url_for(url, app):
    """Allows to use flask.url_for in the test context"""
    with app.app_context():
        return flask.url_for(url, _external=False)


def create_sample_project(id="0001"):
    return {
        "uid": 0,
        "short_name": "Project" + id,
        "comments": "This is a sample project",
        "properties_table": [
            {
                "id": "author",
                "content": "BPM Developers"
            }
        ],
        "active": True
    }
