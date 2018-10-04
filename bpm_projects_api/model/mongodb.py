"""
Models' implementations for Azure
"""


class ProjectDAO(object):
    def __init__(self, db):
        self.db = db

    def get_all(self):
        pass

    def get(self, uid):
        pass

    def create(self, project):
        pass

    def update(self, uid, data):
        pass

    def delete(self, uid):
        pass

    def search(self, search_criteria):
        pass
