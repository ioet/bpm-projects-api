import os

from flask import json
from flask_script import Manager

from bpm_projects_api import create_app
from bpm_projects_api.apis import api

app = create_app()
manager = Manager(app)


@manager.command
def gen_postman_collection(file_path):
    """ Generates a postman collection to make tests """

    data = api.as_postman(urlvars=False, swagger=True)

    if file_path:
        try:
            real_path = os.path.expanduser(file_path)
            with open(real_path, "w") as f:
                f.write(json.dumps(data))
                print("%s was generated successfully" % real_path)
        except OSError as err:
            print("Error while creating '%s': %s" % file_path, err)
    else:
        print(json.dumps(data))


if __name__ == "__main__":
    manager.run()