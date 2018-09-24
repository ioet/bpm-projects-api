import os


class Config:
    DEBUG = False
    OPA_URL = ""


class ProductionConfig(Config):
    SECRET_KEY = os.urandom(16)
    USER_PASSWORD = "secret"


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = "secretkeyfordevelopment"
    USER_PASSWORD = "secret"


class TestingConfig(Config):
    TESTING = True
