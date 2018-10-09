"""
Models' implementations for Azure
"""
import bson
import pymongo
from bson.objectid import ObjectId
from flask import current_app
from flask_pymongo import PyMongo
from pymongo import ReturnDocument

from bpm_projects_api.model.errors \
    import MissingResource, InvalidInput, InvalidMatch

mongo = PyMongo(current_app)


def init_db(app):
    print("Installing MongoDB database...")
    # Indexes
    print("Creating indexes...")
    ProjectDAO.create_indexes()


class ProjectDAO(object):
    collection = mongo.db.projects

    def __init__(self):
        self.collection = ProjectDAO.collection

    @staticmethod
    def create_indexes():
        ProjectDAO.collection.drop_index('search_index')
        ProjectDAO.collection.create_index([
            ('name', pymongo.TEXT),
            ('comments', pymongo.TEXT),
            ('properties.content', pymongo.TEXT),
        ], name='search_index', default_language='english')

    def get_all(self):
        entries = self.collection.find()
        return list(map(convert_from_db, entries))

    def get(self, uid):
        try:
            found_project = self.collection.find_one_or_404({
                "_id": convert_id_to_db(uid)
            })
            return convert_from_db(found_project)
        except bson.errors.InvalidId:
            raise MissingResource("Project '%s' not found" % uid)

    def create(self, project_data):
        project_data['uid'] = None
        new_project = convert_to_db(project_data)

        result = self.collection.insert_one(new_project)
        project_data['uid'] = convert_id_from_db(result.inserted_id)

        return project_data

    def update(self, uid, update_data):
        update_data.pop('uid', None)
        project_update = convert_to_db(update_data)
        try:
            updated_project = self.collection.find_one_and_update(
                {"_id": convert_id_to_db(uid)},
                {'$set': project_update},
                return_document=ReturnDocument.AFTER
            )
            return convert_from_db(updated_project)
        except bson.errors.InvalidId:
            raise MissingResource(
                "Invalid project '%s' could not be updated" % uid
            )

    def delete(self, uid):
        if uid:
            result = self.collection.delete_one({"_id": convert_id_to_db(uid)})
            if result.deleted_count == 0:
                raise MissingResource(
                    "Invalid project '%s' cannot be deleted" % uid
                )

    def flush(self):
        self.collection.delete_many({})

    def search(self, search_criteria):
        if not search_criteria:
            raise InvalidInput("No search criteria specified")

        mongo_search_criteria = dict()
        mongo_search_order = None

        query_str = search_criteria.get('search_string')
        if query_str:
            mongo_search_criteria.update({
                '$text': {
                    '$search': query_str,
                    '$caseSensitive': False,
                    '$diacriticSensitive': True
                },
            })
            mongo_search_order = {'score': {'$meta': 'textScore'}}

        is_active = search_criteria.get('active')
        if is_active is not None:
            mongo_search_criteria.update({
                'is_active': is_active,
            })

        cursor = self.collection.find(mongo_search_criteria, mongo_search_order)

        if query_str:
            cursor.sort([('score', {'$meta': 'textScore'})])

        result = list(map(convert_from_db, cursor))
        if not result:
            raise InvalidMatch("No project matched the specified criteria")

        return result


def convert_to_db(project_json):
    result = {}
    if project_json.get('uid'):
        result['_id'] = convert_id_to_db(project_json['uid'])

    if 'short_name' in project_json:
        result['name'] = project_json['short_name']

    if 'comments' in project_json:
        result['comments'] = project_json['comments']

    if 'properties_table' in project_json:
        result['properties'] = project_json['properties_table']

    if 'active' in project_json:
        result['is_active'] = project_json['active']

    return result


def convert_from_db(project_data):
    result = {}

    if project_data.get('_id'):
        result['uid'] = convert_id_from_db(project_data['_id'])

    if 'name' in project_data:
        result['short_name'] = project_data['name']

    if 'comments' in project_data:
        result['comments'] = project_data['comments']

    if 'properties' in project_data:
        result['properties_table'] = project_data['properties']

    if 'is_active' in project_data:
        result['active'] = project_data['is_active']

    return result


def convert_id_to_db(uid):
    return ObjectId(uid)


def convert_id_from_db(_id):
    return str(_id)


# Instances
project_dao = ProjectDAO()
