import os
from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from .config import Config, TestConfig
import logging.config
from pathlib import Path

file_dir = os.path.split(os.path.realpath(__file__))[0]
logging.config.fileConfig(os.path.join(file_dir, 'logging.ini'), disable_existing_loggers=False, defaults={'logdirectory': os.getenv('LOGGING_DIR')})

db = SQLAlchemy()
api = Api()

logger = logging.getLogger('root')

from .routes import RegionResource

def create_app(testing=False):
    logger.info(f"Creating app with testing {testing}")
    app = Flask(__name__)

    # Config
    env = os.getenv('ENVIRONMENT')
    if testing:
        app.config.from_object(TestConfig())
    else:
        app.config.from_object(Config())

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Resoures
    api.add_resource(RegionResource, '/')

    # Init
    db.init_app(app)
    api.init_app(app)


    with app.app_context():
        db.create_all()
    
    @app.teardown_request
    def teardown_request(exception):
        if exception:
            db.session.rollback()
        db.session.remove()

    @app.errorhandler(500)
    def on_error(error):
        return jsonify({
            'status': 'error',
            'message': 'Internal error'
        }), 500

    return app

    


if __name__ == '__main__':
    app = create_app(True)
    app.run(host="0.0.0.0", port=8000, debug=True)