
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


from .in_memory import ProjectDAO

project_dao = ProjectDAO()

__all__ = [project_dao]
