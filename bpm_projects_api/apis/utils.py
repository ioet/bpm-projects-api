from bpm_projects_api.model.errors import InvalidInput


def query_str(min_length, max_length):
    """String argument with specific dimensions"""

    def validate(s):
        if len(s) < min_length:
            raise InvalidInput("not allowed because it has less than %i "
                               "characters long" % min_length)
        if len(s) > max_length:
            raise InvalidInput("not allowed because it has more than %i "
                               "characters long" % max_length)
        return s

    return validate


def string_is_none(criteria_string):
    if criteria_string is None:
            raise ValueError("The atribute is empty")
    return criteria_string
