import os


class Config:
    DEBUG = False
    OPA_URL = os.environ.get('OPA_URL',
                             'http://0.0.0.0:8181/v1/data/bpm/projects/allow')
    OPA_SECURED = os.environ.get('OPA_SECURED', False) == 'True'
    TOKEN_TTL = 3600
    FLASK_DEBUG = True


class ProductionConfig(Config):
    SECRET_KEY = os.urandom(16)
    USER_PASSWORD = "secret"
    FLASK_ENV = "production"


class InMemoryDevelopmentConfig(Config):
    DEBUG = True
    FLASK_DEBUG = True
    SECRET_KEY = "secretkeyfordevelopment"
    USER_PASSWORD = "secret"
    FLASK_ENV = "development"
    DATABASE = "in_memory"
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS')


class LocalMongoDBDevelopmentConfig(Config):
    DEBUG = False
    OPA_URL = os.environ.get('OPA_URL',
                             'http://0.0.0.0:8181/v1/data/bpm/projects/allow')
    OPA_SECURED = os.environ.get('OPA_SECURED', False) == 'True'
    SECRET_KEY = "secretkeyfordevelopment"
    USER_PASSWORD = "secret"
    FLASK_ENV = "development"
    DATABASE = "mongodb"
    MONGO_URI = 'mongodb://localhost:27017/ioet-bpm'


class TestConfig(InMemoryDevelopmentConfig):
    DEBUG = True
    TESTING = True
    SERVER_NAME = "localhost"
    TEST_USER = "testuser@domain.com"
    SECRET_KEY = "secretkeyfordevelopment"
    USER_PASSWORD = "secret"
    FLASK_ENV = "development"
    DATABASE = "in_memory"


class AzureConfig(Config):
    SECRET_KEY = "secret"
    OPA_URL = os.environ.get('OPA_URL',
                             'http://0.0.0.0:8181/v1/data/bpm/projects/allow')
    OPA_SECURED = os.environ.get('OPA_SECURED', False) == 'True'
    DATABASE = "mongodb_cosmosdb"
    TOKEN_TTL = 3600
    MONGO_URI = os.environ.get('DB_URI')
    FLASK_DEBUG = False
    DEBUG = False


class AzureDevelopmentConfig(AzureConfig, LocalMongoDBDevelopmentConfig):
    CORS_ORIGINS = "*"


class AzureProductionConfig(AzureConfig, ProductionConfig):
    DEBUG = False
    FLASK_DEBUG = False
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS')


class TestAzureConfig(AzureConfig, TestConfig):
    OPA_SECURED = False


class TestLocalMongoDBConfig(LocalMongoDBDevelopmentConfig, TestConfig):
    MONGO_URI = 'mongodb://localhost:27017/ioet-bpm-test'
    OPA_SECURED = False
