import os


class Config:
    DEBUG = False
    OPA_URL = ""
    DATABASE = "in_memory"


class ProductionConfig(Config):
    SECRET_KEY = os.urandom(16)
    USER_PASSWORD = "secret"
    FLASK_ENV = "production"


class DevelopmentConfig(Config):
    DEBUG = True
    SECRET_KEY = "secretkeyfordevelopment"
    USER_PASSWORD = "secret"
    FLASK_ENV = "development"


class TestingConfig(DevelopmentConfig):
    DEBUG = True
    TESTING = True
    SERVER_NAME = "localhost"
    TEST_USER = "testuser@domain.com"


class AzureConfig(Config):
    DATABASE = "mongodb"
    DATABASE_NAME = 'ioet-bpm'


class AzureDevelopmentConfig(DevelopmentConfig, AzureConfig):
    MONGO_URI = 'mongodb://localhost:27017/'


class AzureProductionConfig(ProductionConfig, AzureConfig):
    pass
