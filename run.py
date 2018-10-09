"""
This file is needed by gunicorn to run
"""
import os
from bpm_projects_api import create_app

config = os.environ.get('APP_CONFIG', 'bpm_projects_api.config.ProductionConfig')

app = create_app(config)
print("BPM Projects API server is running")
