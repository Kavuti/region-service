import os
import logging
from flask import Flask, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_marshmallow import Marshmallow
from .config import Config, TestConfig

db = SQLAlchemy()
api = Api()
ma = Marshmallow()

logger = logging.getLogger('root')

from .routes import RegionResource

def create_app(testing=False):

    logger.info(f"Creating app with testing {testing}")
    app = Flask(__name__)

    # Config
    if testing:
        app.config.from_object(TestConfig())
    else:
        app.config.from_object(Config())

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Resoures
    api.add_resource(RegionResource, '/regions')

    # Init
    db.init_app(app)
    api.init_app(app)
    ma.init_app(app)


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
    
    @app.errorhandler(400)
    def on_fail(fail):
        return jsonify({
            'status': 'fail',
            'message': fail
        }), 400

    return app

    


if __name__ == '__main__':
    app = create_app(True)
    app.run(host="0.0.0.0", port=8000, debug=True)