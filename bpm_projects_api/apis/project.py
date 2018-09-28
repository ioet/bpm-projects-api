from flask_restplus import Resource
from bpm_projects_api.core.security import token_required, token_policies
from .models import search_model, project, metadata, ns
from .dao import dao

ns = Namespace('projects', description='Operations for projects of the BPM')

# Project property
metadata = ns.model('Metadata', {
    'id': fields.String(required=True, title="Key"),
    'content': fields.String(title="Value")
})

# Project model for the API
project = ns.model('Project', {
    'uid': fields.String(readOnly=True, required=True, title='Identifier',
                         description='The project generated unique id'),
    'short_name': fields.String(required=True, title='Short name',
                                description='Unique name in the system'),
    'comments': fields.String(title='Comments',
                              description='Comments about the project'),
    'properties_table': fields.List(fields.Nested(metadata)),
    'active': fields.Boolean(title='Is active?',
                             description='Whether the project is active '
                                         'or not')
})


class ProjectDAO(object):
    def __init__(self):
        self.counter = 0
        self.projects = []

    def get(self, id):
        for project in self.projects:
            if project['uid'] == id:
                return project
        ns.abort(404, "The project {} doesn't exist".format(id))

    def create(self, project):
        self.counter += 1
        project['uid'] = str(self.counter)
        self.projects.append(project)
        return project

    def update(self, id, data):
        project = self.get(id)
        project.update(data)
        return project

metadata = metadata
project = project
search_model = search_model


@ns.route('/')
@ns.doc()
class Projects(Resource):
    """Shows a list of all projects"""

    @ns.doc('list_projects')
    @ns.marshal_list_with(project, code=200)
    @token_required
    @token_policies.administrator_required
    def get(self):
        """List all projects"""
        return dao.projects

    @ns.doc('create_project')
    @ns.expect(project)
    @ns.marshal_with(project, code=201)
    @token_policies.administrator_required
    def post(self):
        """Create a project"""
        return dao.create(ns.payload), 201


@ns.route('/<uid>')
@ns.response(404, 'Project not found')
@ns.param('uid', 'The project identifier')
@ns.doc()
class Project(Resource):
    """To show a project or delete it"""

    @ns.doc('get_project')
    @ns.marshal_with(project)
    def get(self, uid):
        """Fetch a given project"""
        return dao.get(uid)

    @ns.doc('delete_project')
    @ns.response(204, 'Project deleted')
    @token_policies.administrator_required
    def delete(self, uid):
        """Delete a project given its identifier"""
        dao.delete(uid)
        return None, 204

    @ns.doc('put_project')
    @ns.expect(project)
    @ns.marshal_with(project)
    @token_policies.administrator_required
    def patch(self, uid):
        """Update a project given its identifier"""
        return dao.update(uid, ns.payload)


@ns.route('/search/')
@ns.response(404, 'Project not found')
class SearchProject(Resource):
    """To search for projects"""

    @ns.doc('search_project')
    @ns.expect(search_model)
    @ns.marshal_list_with(project, code=200)
    def post(self):
        """Fetch projects given a string"""
        return dao.search(ns.payload)


@ns.route('/status/activate/<uid>')
@ns.response(404, 'Project not found')
@ns.param('uid', 'The project identifier')
class ActivateProject(Resource):
    """To set a project active"""

    @ns.doc('set_project_active')
    @token_policies.administrator_required
    @ns.marshal_list_with(project, code=200)
    @ns.response(205, 'Project status changed')
    def patch(self, uid):
        """Set projects active given a string"""
        return dao.activate(uid)


@ns.route('/status/deactivate/<uid>')
@ns.response(404, 'Project not found')
@ns.param('uid', 'The project identifier')
class DeactivateProject(Resource):
    """To set a project inactive"""

    @ns.doc('set_project_inactive')
    @token_policies.administrator_required
    @ns.marshal_list_with(project, code=200)
    @ns.response(205, 'Project status changed')
    def patch(self, uid):
        """Set projects inactive given a string"""
        return dao.deactivate(uid)
