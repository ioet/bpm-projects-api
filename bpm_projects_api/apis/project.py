from flask_restplus import fields, Resource, Namespace, abort, inputs
# Project namespace
from flask_restplus.fields import Raw

from bpm_projects_api.apis.dao import ProjectDAO
from bpm_projects_api.core.security import token_required, token_policies, MissingResource

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

# Search model
search_model = ns.model('SearchCriteria', {
    'search_string': fields.String(title='Keywords',
                                   description='What you want to search for in the comments/the name'),
    'active': fields.Boolean(title='Is active?',
                             description='true=only active, false=only inactive, none=all'),
})


def field_payload(name, field: Raw):
    """Returns a field to be used as payload"""
    return ns.model(name, {'value': field})


dao = ProjectDAO()


@ns.route('/')
class Projects(Resource):
    """Shows a list of all projects"""

    @ns.doc('list_projects')
    @ns.marshal_list_with(project, code=200)
    @token_required
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


@ns.route('/<string:uid>')
@ns.response(404, 'Project not found')
@ns.param('uid', 'The project identifier')
class Project(Resource):
    """To show a project or delete it"""

    @ns.doc('get_project')
    @ns.marshal_with(project)
    def get(self, uid):
        """Retrieve a project"""
        return dao.get(uid)

    @ns.doc('delete_project')
    @ns.response(204, 'Project deleted')
    @token_policies.administrator_required
    def delete(self, uid):
        """Deletes a project"""
        dao.delete(uid)
        return None, 204

    @ns.doc('put_project')
    @ns.expect(project)
    @ns.marshal_with(project)
    @token_policies.administrator_required
    def put(self, uid):
        """Add or replace a project"""
        return dao.update(uid, ns.payload)


@ns.route('/search/')
@ns.response(404, 'Project not found')
class SearchProject(Resource):
    @ns.doc('search_project', body='Search a project in the system')
    @ns.expect(search_model)
    @ns.marshal_list_with(project, code=200)
    def post(self):
        """Search for projects given some criteria(s)"""
        return dao.search(ns.payload)


activePropertyParser = ns.parser()
activePropertyParser.add_argument('active',
                                  type=inputs.boolean,
                                  location='form',
                                  required=True,
                                  help='Is the project active?')


@ns.route('/<string:uid>/active')
@ns.param('uid', 'The project identifier')
@ns.param('active', 'Is the project active?', 'formData')
@ns.response(404, 'Project not found')
@ns.response(204, 'Status of the project successfully updated')
class ProjectStatus(Resource):

    @ns.doc('update_project_status')
    @ns.expect(activePropertyParser)
    @token_policies.administrator_required
    def post(self, uid):
        """Updates the project active status"""
        try:
            args = activePropertyParser.parse_args()
            dao.activate(uid, args['active'])
            return None, 204
        except ValueError:
            abort(message="value is missing", code=400)
        except MissingResource as error:
            abort(message=error, code=400)
