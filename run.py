from bpm_projects_api import create_app

from bpm_projects_api import config

app = create_app(config_object='bpm_projects_api.config.DevelopmentConfig')
print("BPM Projects API server running")
