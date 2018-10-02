from bpm_projects_api.model import MissingResource, InvalidInput, InvalidMatch


class ProjectDAO(object):
    def __init__(self):
        self.counter = 0
        self.projects = []

    def get(self, uid):
        for project in self.projects:
            if project.get('uid') == uid:
                return project
        raise MissingResource("Project '%s' not found" % uid)

    def create(self, project):
        self.counter += 1
        project['uid'] = str(self.counter)
        self.projects.append(project)
        return project

    def update(self, uid, data):
        project = self.get(uid)
        if project:
            project.update(data)
            return project
        else:
            raise MissingResource("Project '%s' not found" % uid)

    def delete(self, uid):
        project = self.get(uid)
        self.projects.remove(project)

    def search(self, search_criteria):
        matching_projects = self.select_matching_projects(search_criteria)

        if len(matching_projects) > 0:
            return matching_projects
        else:
            raise InvalidMatch("No project matched the specified criteria")

    def select_matching_projects(self, search_criteria):
        def matches_search_string(search_str, project):
            return search_str in project['comments'] or \
                   search_str in project['short_name']

        if not search_criteria:
            raise InvalidInput("No search criteria specified")

        if 'search_string' in search_criteria:
            search_str = search_criteria['search_string']
            matching_projects = [p for p
                                 in self.projects
                                 if matches_search_string(search_str, p)]
        else:
            matching_projects = self.projects

        if 'active' in search_criteria:
            matching_projects = [p for p
                                 in matching_projects
                                 if p['active'] is search_criteria['active']]

        return matching_projects
