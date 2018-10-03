class MissingResource(Exception):
    """
    Errors related to missing resource in the system
    """
    pass


class InvalidInput(Exception):
    """
    Errors related to an invalid input coming from the user
    """
    pass


class InvalidMatch(Exception):
    """
    Errors related to an invalid match during a search
    """
    pass


project_dao = None


def init_app(app):
    database_strategy_name = app.config['DATABASE']
    globals()["use_%s" % database_strategy_name](app)


def use_in_memory(app):
    global project_dao
    from .in_memory import ProjectDAO
    project_dao = ProjectDAO()


def use_azure(app):
    global project_dao
    from flask_pymongo import PyMongo
    from .mongodb import ProjectDAO
    mongo = PyMongo(app)
    project_dao = ProjectDAO()
