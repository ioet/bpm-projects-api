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
        if not search_criteria:
            raise InvalidInput("No search criteria specified")

        mongo_search_criteria = dict()
        mongo_search_order = None

        query_str = search_criteria.get('search_string')
        if query_str:
            mongo_search_criteria.update({
                '$or': [
                    {'name': {'$regex': query_str}},
                    {'comments': {'$regex': query_str}},
                    {"properties": {'$elemMatch': {
                        'content': {'$regex': query_str}
                    }}}
                ]
            })

        is_active = search_criteria.get('active')
        if is_active is not None:
            mongo_search_criteria.update({
                'is_active': is_active,
            })

        cursor = self.collection.find(mongo_search_criteria)

        result = list(map(convert_from_db, cursor))
        if not result:
            raise InvalidMatch("No project matched the specified criteria")

        return result


# Instances
project_dao = ProjectDAO()
