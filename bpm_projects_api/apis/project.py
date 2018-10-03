from flask_restplus import fields, Resource, Namespace, abort, inputs

from bpm_projects_api.core.security import token_required, token_policies
from bpm_projects_api.model import project_dao

# Project namespace

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
    'search_string': fields.String(
        title='Keywords',
        description='What you want to search for in the comments/the name'
    ),
    'active': fields.Boolean(title='Is active?',
                             description='true|false the project is active'),
})


@ns.route('/')
class Projects(Resource):
    @ns.doc('list_projects')
    @ns.marshal_list_with(project, code=200)
    @token_required
    def get(self):
        """List all projects"""
        return project_dao.get_all()

    @ns.doc('create_project')
    @ns.expect(project)
    @ns.marshal_with(project, code=201)
    @token_policies.administrator_required
    def post(self):
        """Create a project"""
        return project_dao.create(ns.payload), 201


@ns.route('/<string:uid>')
@ns.response(404, 'Project not found')
@ns.param('uid', 'The project identifier')
class Project(Resource):
    @ns.doc('get_project')
    @ns.marshal_with(project)
    def get(self, uid):
        """Retrieve a project"""
        return project_dao.get(uid)

    @ns.doc('delete_project')
    @ns.response(204, 'Project deleted')
    @token_policies.administrator_required
    def delete(self, uid):
        """Deletes a project"""
        project_dao.delete(uid)
        return None, 204

    @ns.doc('put_project')
    @ns.expect(project)
    @ns.marshal_with(project)
    @token_policies.administrator_required
    def put(self, uid):
        """Create or replace a project"""
        return project_dao.update(uid, ns.payload)


@ns.route('/search/')
@ns.response(404, 'Project not found')
class SearchProject(Resource):
    @ns.doc('search_project')
    @ns.expect(search_model)
    @ns.marshal_list_with(project, code=200)
    def post(self):
        """Search for projects given some criteria(s)"""
        return project_dao.search(ns.payload)


project_update_parser = ns.parser()
project_update_parser.add_argument('active',
                                   type=inputs.boolean,
                                   location='form',
                                   required=True,
                                   help='Is the project active?')


@ns.route('/<string:uid>')
@ns.param('uid', 'The project identifier')
@ns.param('active', 'Is the project active?', 'body')
@ns.response(404, 'Project not found')
@ns.response(204, 'State of the project successfully updated')
@ns.response(400, "Bad parameters input")
class ChangeProjectState(Resource):
    @ns.doc('update_project_status')
    @ns.expect(project_update_parser)
    @token_policies.administrator_required
    def post(self, uid):
        """Updates a project using form data"""
        try:
            args = project_update_parser.parse_args()
            update_data = {
                "active": args["active"]
            }
            project_dao.update(uid, update_data)
            return None, 204
        except ValueError:
            abort(code=400)
