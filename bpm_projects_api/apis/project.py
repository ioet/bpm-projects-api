from flask_restplus import fields, Resource, Namespace
# Project namespace
from bpm_projects_api.core.security import token_required, token_policies

ns = Namespace('projects', description='Operations for projects of the BPM')

# Project property
metadata = ns.model('Metadata', {
    'id': fields.String(required=True, title="Key"),
    'content': fields.String(title="Value")
})

# Project model for the API
project = ns.model('Project', {
    'uid': fields.String(readOnly=True, required=True, title='Identifier',
                         description='The project generated unique identifier'),
    'short_name': fields.String(required=True, title='Short name', description='Unique name in the system'),
    'comments': fields.String(title='Comments', description='Comments about the project'),
    'properties_table': fields.List(fields.Nested(metadata)),
    'active': fields.Boolean(title='Is active?', description='Whether the project is active or not'),
})

search_model = ns.model('SearchCriteria', {
    'search_string': fields.String(title='Keywords',
                                   description='What you want to search for in the comments/the name'),
    'active': fields.Boolean(title='Is active?',
                             description='true=only active, false=only inactive, none=all'),
})


class ProjectDAO(object):
    def __init__(self):
        self.counter = 0
        self.projects = []

    def get(self, id):
        for project in self.projects:
            if project['uid'] == id:
                return project
        return '', 404

    def create(self, project):
        self.counter += 1
        project['uid'] = str(self.counter)
        self.projects.append(project)
        return project

    def update(self, id, data):
        project = self.get(id)
        project.update(data)
        return project

    def delete(self, id):
        project = self.get(id)
        self.projects.remove(project)

    def search(self, search_criteria):
        matching_projects = self.select_matching_projects(search_criteria)

        if len(matching_projects) > 0:
            return matching_projects
        else:
            return '', 404

    def deactivate(self, project_id):
        temp_project = self.get(project_id)
        if temp_project == ('', 404):
            return '', 404
        elif temp_project['active'] is True:
            temp_project['active'] = False
            return temp_project
        else:
            return '', 404

    def activate(self, project_id):
        temp_project = self.get(project_id)
        if temp_project == ('', 404):
            return '', 404
        elif temp_project['active'] is False:
            temp_project['active'] = True
            return temp_project
        else:
            return '', 404

    @staticmethod
    def select_matching_projects(search_criteria):
        search_string = None
        active = None

        if 'search_string' in search_criteria:
            search_string = search_criteria['search_string']
        if 'active' in search_criteria:
            active = search_criteria['active']

        if search_string is None and active is None:
            return 'No data sent', 404

        if search_string:
            matching_projects = [temp_project for temp_project in dao.projects
                                 if (search_string in temp_project['comments'] or
                                     search_string in temp_project['short_name'])]
        else:
            matching_projects = [temp_project for temp_project in dao.projects]

        if active is True or active is False:
            projects_to_remove = [temp_project for temp_project in matching_projects
                                  if temp_project['active'] is not active]

            for temp_project in projects_to_remove:
                matching_projects.remove(temp_project)

        return matching_projects


dao = ProjectDAO()


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
