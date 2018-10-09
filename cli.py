import os

from flask import json
from flask_script import Manager

from bpm_projects_api import create_app
from bpm_projects_api.apis import api

config = os.environ.get('APP_CONFIG', 'bpm_projects_api.config.DevelopmentConfig')
app = create_app(config)
manager = Manager(app)
print("BPM Projects API created for configuration '%s'" % config)


@manager.command
def gen_postman_collection(filename=None):
    """ Generates a postman collection to make tests """
    data = api.as_postman(urlvars=False, swagger=True)

    if filename:
        try:
            real_path = os.path.expanduser(filename)
            with open(real_path, "w") as f:
                f.write(json.dumps(data))
                print("%s was generated successfully" % real_path)
        except OSError as err:
            print("Error while creating '%s': %s" % filename, err)
    else:
        print(json.dumps(data))


@manager.command
def init_db():
    """Initializes the database"""
    from bpm_projects_api.model import init_db
    init_db(app)


if __name__ == "__main__":
    manager.run()
