from flask import Flask
from werkzeug.contrib.fixers import ProxyFix
from bpm_projects_api import config
from bpm_projects_api.apis import api


app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api.init_app(app)


if __name__ == '__main__':
    app.run(debug=config.FLASK_DEBUG)
