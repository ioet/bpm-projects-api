import os


class Config:
    DEBUG = False
    OPA_URL = ""


class ProductionConfig(Config):
    SECRET_KEY = os.urandom(16)
    SERVER_NAME = "0.0.0.0:8000"


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = "secretkeyfordevelopment"
    USER_PASSWORD = "secret"
    OPA_URL = ""


class TestingConfig(Config):
    TESTING = True
