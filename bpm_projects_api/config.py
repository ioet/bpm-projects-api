import os


class Config:
    DEBUG = False
    OPA_URL = ""


class ProductionConfig(Config):
    SECRET_KEY = os.urandom(16)
    USER_PASSWORD = "secret"
    FLASK_ENV = "production"


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = "secretkeyfordevelopment"
    USER_PASSWORD = "secret"
    FLASK_ENV = "development"


class TestingConfig(Config):
    TESTING = True
    SECRET_KEY = "secretkeyfordevelopment"
    USER_PASSWORD = "secret"
    SERVER_NAME = "localhost"
    TEST_USER = "testuser@domain.com"
    FLASK_ENV = "development"
