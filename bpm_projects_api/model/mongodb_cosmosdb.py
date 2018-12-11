import re

from bpm_projects_api.model.errors import InvalidInput, InvalidMatch
from .mongodb import ProjectDAO as ProjectDaoMongoDB, convert_from_db


def init_db(app):
    app.logger.info("Installing MongoDB database in Azure Cosmos DB...")
    # Indexes
    app.logger.info("Creating indexes...")
    ProjectDAO.create_indexes(app)


class ProjectDAO(ProjectDaoMongoDB):
    @staticmethod
    def create_indexes(app):
        """It has to be done in the Azure portal"""
        pass

    def search(self, search_criteria):
        mongo_search_criteria = dict()

        query_str = search_criteria.get('search_string', '')
        if query_str:
            query_str_content = query_str.strip()
            if query_str_content:
                query_str_re = re.compile(query_str_content, re.IGNORECASE)
                mongo_search_criteria.update({
                    '$or': [
                        {'name': {'$regex': query_str_re}},
                        {'comments': {'$regex': query_str_re}},
                        {"properties": {'$elemMatch': {
                            'content': {'$regex': query_str_re}
                        }}}
                    ]
                })

        is_active = search_criteria.get('active')
        if is_active is not None:
            mongo_search_criteria.update({
                'is_active': is_active,
            })

        if not mongo_search_criteria:
            raise InvalidInput("No search criteria specified")

        cursor = self.collection.find(mongo_search_criteria)

        result = list(map(convert_from_db, cursor))
        if not result:
            raise InvalidMatch("No project matched the specified criteria")

        return result
    
    def search_filtered_projects(self, search_criteria):
        mongo_search_criteria = dict()

        query_str = search_criteria.get('short_name', '')
        if query_str:
            query_str_content = query_str.strip()
            if query_str_content:
                query_str_re = re.compile(query_str_content, re.IGNORECASE)
                mongo_search_criteria.update({
                    '$or': [
                        {'name': {'$regex': query_str_re}}
                    ]
                })

        is_active = search_criteria.get('active')
        if is_active is not None:
            mongo_search_criteria.update({
                'is_active': is_active,
            })

        cursor = self.collection.find(mongo_search_criteria)

        result = list(map(convert_from_db, cursor))

        return result

# Instances
project_dao = ProjectDAO()
