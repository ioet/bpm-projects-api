from flask_restplus import fields, Resource, Namespace
# from flask import Blueprint, render_template, abort

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

# active component to change the status of a project
search_criteria = ns.model('Search_Criteria', {
    'active': fields.Boolean(title='Is active?', description='If true, only active projects will be respected'),
    'search_string': fields.String(title='Keywords',
                                   description='What you want to search for in the comments/the name'),
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

    def delete(self, id):
        project = self.get(id)
        self.projects.remove(project)

    def search(self, data):
        matching_projects = [project for project in dao.projects if (data['search_string'] in str(project['comments']) or
                                                                     data['search_string'] in str(project['short_name']))]
        # if active is true, only display active projects
        if(len(matching_projects) > 0):
            if(data['active'] == ('true' or 'TRUE' or 'True')):
                for project in matching_projects:
                    if project['active'] == True:
                        pass
                    else:
                        matching_projects.remove(project)

            # otherwise return all objects that match the search string
                if(len(matching_projects) > 0):
                    return matching_projects
                else:
                    ns.abort(404, "No matching projects found")

            return matching_projects
        else:
            ns.abort(404, "No matching projects found")


    def change_status(self, data):
        matching_projects = [project for project in dao.projects if (data['search_string'] in str(project['comments']) or
                                                                     data['search_string'] in str(project['short_name']))]

        if(len(matching_projects) > 0):
            # if the user wants to set the data of found projects to false do so
            if(data['active'] == ('false' or 'FALSE' or 'False')):
                for project in matching_projects:
                    project['active'] = data['active']

            for original_project in dao.projects:
                for project in matching_projects:
                    if(project['uid'] == original_project['uid']):
                        original_project = project

            return matching_projects
        else:
            ns.abort(404, "No projects matching {} found".format(data['search_string']))


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


# route is chosen because of the example above the "T odo" class on
# https://flask-restplus.readthedocs.io/en/0.11.0/example.html and
# https://www.rithmschool.com/courses/flask-fundamentals/routing-with-flask
# "<url>/<<data_type>:<variable_name>>
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
    def put(self, uid):
        """Update a project given its identifier"""
        return dao.update(uid, ns.payload)


# route is chosen because of the example above the "T odo" class on
# https://flask-restplus.readthedocs.io/en/0.11.0/example.html and
# https://www.rithmschool.com/courses/flask-fundamentals/routing-with-flask
# "<url>/<<data_type>:<variable_name>>
@ns.route('/search/<data>')
@ns.response(404, 'Project not found')
class SearchProject(Resource):
    """To search for projects and change their status"""

    @ns.doc('search_project')
    @ns.expect(search_criteria)
    @ns.response(210, 'Project found')
    @ns.marshal_with(search_criteria)
    def put(self, data):
        """Fetch projects given a string"""
        return dao.search(ns.payload)


@ns.route('/change/')
@ns.response(404, 'Project not found')
class ChnageProject(Resource):
    """To change a projects active status"""

    @ns.doc('set_project_inactive')
    @ns.expect(search_criteria)
    @ns.marshal_with(search_criteria)
    @token_policies.administrator_required
    def put(self):
        """Set projects active/inactive"""
        return dao.change_status(ns.payload)