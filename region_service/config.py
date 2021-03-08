import os
import logging.config

class Config:
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')

    def __init__(self):
        file_dir = os.path.split(os.path.realpath(__file__))[0]
        logging.config.fileConfig(os.path.join(file_dir, 'logging.ini'), disable_existing_loggers=False, defaults={'logdirectory': os.getenv('LOGGING_DIR')})

class TestConfig():
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'