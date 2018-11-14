#!/usr/bin/env python3
"""
This file is needed by gunicorn to run
"""
import os
from bpm_projects_api import create_app

config = os.environ.get('APP_CONFIG', 'bpm_projects_api.config.LocalMongoDBDevelopmentConfig')

app = create_app(config)
print("BPM Projects API server was created")