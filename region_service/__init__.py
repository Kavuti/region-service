import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from .config import Config, TestConfig
import logging.config
from pathlib import Path

file_dir = os.path.split(os.path.realpath(__file__))[0]
logging.config.fileConfig(os.path.join(file_dir, 'logging.ini'), disable_existing_loggers=False)

db = SQLAlchemy()
ma = Marshmallow()

logger = logging.getLogger('root')

from .routes import regions

def create_app(testing=False):
    logger.info(f"Creating app with testing {testing}")
    app = Flask(__name__)

    env = os.getenv('ENVIRONMENT')
    if testing:
        app.config.from_object(TestConfig())
    else:
        app.config.from_object(Config())

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.register_blueprint(regions)

    db.init_app(app)
    ma.init_app(app)

    with app.app_context():
        db.create_all()

    return app

