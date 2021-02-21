import os

class Config:
    TESTING = False
    DATABASE_URI = os.getenv('DATABASE_URI')
    SQLALCHEMY_DATABASE_URI = DATABASE_URI

class TestConfig(Config):
    TESTING = True
    DATABASE_URI = 'sqlite://'
    SQLALCHEMY_DATABASE_URI = DATABASE_URI