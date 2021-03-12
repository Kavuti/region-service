import os
import logging
from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
from .config import Config, TestConfig
from marshmallow import ValidationError
from .utils import *

db = SQLAlchemy()
api = Api()
ma = Marshmallow()
migrate = Migrate(db=db)

logger = logging.getLogger('root')

from .routes import RegionResource, HealthcheckResource

def create_app(testing=False):

    app = Flask(__name__)

    # Config
    if testing:
        app.config.from_object(TestConfig())
    else:
        app.config.from_object(Config())

    logging.info(f"Creating app with testing {testing}")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Resoures
    api.add_resource(RegionResource, '/')
    api.add_resource(HealthcheckResource, '/health')

    # Init
    db.init_app(app)
    api.init_app(app)
    ma.init_app(app)
    migrate.init_app(app)

    with app.app_context():
        db.create_all()
    
    @app.teardown_request
    def teardown_request(exception):
        if exception:
            db.session.rollback()
        db.session.remove()

    @app.errorhandler(ValidationError)
    def handle_validation_error(e):
        logger.error("Error during entity validation", e)
        return make_response(fail(e.messages))


    @app.errorhandler(422)
    def handle_validation_error(e):
        logger.error("Error during entity processing", e)
        return make_response(fail("Some data is not valid"))

    return app

    


if __name__ == '__main__':
    app = create_app(True)
    app.run(host="0.0.0.0", port=8000, debug=True)