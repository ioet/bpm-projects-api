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
    FLASK_DEBUG = True
    SECRET_KEY = "secretkeyfordevelopment"
    USER_PASSWORD = "secret"
    FLASK_ENV = "development"
    DATABASE = "in_memory"


class TestConfig(DevelopmentConfig):
    DEBUG = True
    TESTING = True
    SERVER_NAME = "localhost"
    TEST_USER = "testuser@domain.com"


class AzureConfig(Config):
    DATABASE = "mongodb"


class AzureDevelopmentConfig(AzureConfig, DevelopmentConfig):
    MONGO_URI = 'mongodb://localhost:27017/ioet-bpm'


class AzureProductionConfig(ProductionConfig, AzureConfig):
    DEBUG = True
    MONGO_URI = os.environ.get('DB_URI')


class TestAzureDevelopmentConfig(AzureConfig, TestConfig):
    MONGO_URI = 'mongodb://localhost:27017/ioet-bpm-test'
