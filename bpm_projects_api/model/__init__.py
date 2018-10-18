project_dao = None
init_db = None


def init_app(app):
    database_strategy_name = app.config['DATABASE']
    with app.app_context():
        module = globals()["use_%s" % database_strategy_name]()
        global project_dao, init_db
        init_db = module.init_db
        project_dao = module.project_dao


def use_in_memory():
    import bpm_projects_api.model.in_memory as module
    return module


def use_mongodb():
    import bpm_projects_api.model.mongodb as module
    return module


def use_mongodb_cosmosdb():
    import bpm_projects_api.model.mongodb_cosmosdb as module
    return module
