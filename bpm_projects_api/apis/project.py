from flask_restplus import fields, Resource, Namespace, abort, inputs

from bpm_projects_api.apis.utils import query_str
# Project namespace
from bpm_projects_api.model import project_dao
from bpm_projects_api.model.errors import MissingResource

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


@ns.route('/')
class Projects(Resource):
    @ns.doc('list_projects')
    @ns.marshal_list_with(project, code=200)
    def get(self):
        """List all projects"""
        return project_dao.get_all()

    @ns.doc('create_project')
    @ns.expect(project)
    @ns.marshal_with(project, code=201)
    def post(self):
        """Create a project"""
        return project_dao.create(ns.payload), 201


search_parser = ns.parser()
search_parser.add_argument('search_string',
                           type=query_str(3, 100),
                           help='Text to search in the project')
search_parser.add_argument('active',
                           help='Is active?',
                           type=inputs.boolean)


@ns.route('/search/')
@ns.response(204, 'No match for your search')
@ns.response(400, "Bad input of search parameters")
class SearchProject(Resource):
    @ns.doc('search_project')
    @ns.expect(search_parser)
    @ns.marshal_list_with(project, code=200)
    def get(self):
        """Search for projects given some criteria(s)"""
        search_data = search_parser.parse_args()
        return project_dao.search(search_data)


project_update_parser = ns.parser()
project_update_parser.add_argument('active',
                                   type=inputs.boolean,
                                   location='form',
                                   required=True,
                                   help='Is the project active?')


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
    def delete(self, uid):
        """Deletes a project"""
        project_dao.delete(uid)
        return None, 204

    @ns.doc('put_project')
    @ns.expect(project)
    @ns.marshal_with(project)
    def put(self, uid):
        """Create or replace a project"""
        return project_dao.update(uid, ns.payload)

    @ns.doc('update_project_status')
    @ns.param('uid', 'The project identifier')
    @ns.response(204, 'State of the project successfully updated')
    @ns.response(400, "Bad parameters input")
    @ns.expect(project_update_parser)
    def post(self, uid):
        """Updates a project using form data"""
        try:
            update_data = project_update_parser.parse_args()
            return project_dao.update(uid, update_data), 200
        except ValueError:
            abort(code=400)
        except MissingResource as e:
            abort(message=str(e), code=404)
