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
    globals()["use_%s" % database_strategy_name]()


def use_in_memory():
    global project_dao
    from .in_memory import ProjectDAO
    project_dao = ProjectDAO()


def use_azure():
    global project_dao
    from .azure import ProjectDAO
    project_dao = ProjectDAO()
