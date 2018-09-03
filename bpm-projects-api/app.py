from flask import Flask
from flask_restplus import Api, fields, Resource
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
api = Api(app, version='0.0.1',
          title='BPM API',
          description='API for BPM Projects')

ns = api.namespace('projects', description='Project operations')

property = api.model('Property', {
    'id': fields.String,
    'content': fields.String
})

# Project model to marshall and unmarshall responses and requests
project = api.model('Project', {
    'guid': fields.Integer(readOnly=True, title='Identifier', description='The project generated unique identifier'),
    'short_name': fields.String(required=True, title='Short name', description='The task details'),
    'comments': fields.String(title='Comments', description='Comments about the project'),
    'properties_table': fields.List(fields.Nested(property)),
    'active': fields.Boolean(title='Is active?', description='Whether the project is active or not'),
})


class ProjectDAO(object):
    def __init__(self):
        self.counter = 0
        self.projects = []

    def get(self, id):
        for project in self.projects:
            if project['guid'] == id:
                return project
        api.abort(404, "The project {} doesn't exist".format(id))

    def create(self, project):
        project['guid'] = self.counter = self.counter + 1
        self.projects.append(project)
        return project

    def update(self, id, data):
        project = self.get(id)
        project.update(data)
        return project

    def delete(self, id):
        project = self.get(id)
        self.projects.remove(project)


dao = ProjectDAO()


@ns.route('/')
class Projects(Resource):
    """Shows a list of all projects"""

    @ns.doc('list_projects')
    @ns.marshal_list_with(project)
    def get(self):
        """List all projects"""
        return dao.projects

    @ns.doc('create_project')
    @ns.expect(project)
    @ns.marshal_with(project, code=201)
    def post(self):
        """Create a project"""
        return dao.create(api.payload), 201


@ns.route('/<int:guid>')
@ns.response(404, 'Project not found')
@ns.param('guid', 'The project identifier')
class Project(Resource):
    """To show a project or delete it"""

    @ns.doc('get_project')
    @ns.marshal_with(project)
    def get(self, guid):
        """Fetch a given project"""
        return dao.get(guid)

    @ns.doc('delete_project')
    @ns.response(204, 'Project deleted')
    def delete(self, guid):
        """Delete a project given its identifier"""
        dao.delete(guid)
        return None, 204

    @ns.expect(project)
    @ns.marshal_with(project)
    def put(self, guid):
        """Update a project given its identifier"""
        return dao.update(guid, api.payload)


if __name__ == '__main__':
    app.run(debug=True)
