from bpm_projects_api.core.security import MissingResource


class ProjectDAO(object):
    def __init__(self):
        self.counter = 0
        self.projects = []

    def get(self, id):
        for project in self.projects:
            if project.get('uid') == id:
                return project

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

    def activate(self, uid: str, isActive: bool):
        project = self.get(uid)
        if (project):
            project['active'] = isActive
        else:
            raise MissingResource("project '%s' doesnt exist" % uid)


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
