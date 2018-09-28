"""
This file is needed by gunicorn to run
"""
from bpm_projects_api import create_app


app = create_app(config_object='bpm_projects_api.config.ProductionConfig')
print("BPM Projects API server is running")
