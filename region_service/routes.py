from flask import jsonify, request, make_response
from flask_restful import Resource
from .model.region import RegionSchema, region_args
from .workers.region_worker import RegionWorker
from webargs.flaskparser import use_kwargs, use_args
from webargs import fields
from .utils import *
from flask import request
from . import db
from marshmallow import ValidationError
import logging
import time

logger = logging.getLogger('root')

class HealthcheckResource(Resource):
    def get(self):
        try:
            res = db.engine.execute("SELECT 1;")
            return make_response(jsonify({
                'db': True,
                'timestamp': time.time()
            }), 200)
        except:
            return make_response(jsonify({
                'db': False,
                'timestamp': time.time()
            }), 500)

class RegionResource(Resource):

    @use_kwargs(region_args, location="query")
    def get(self, **kwargs):
        worker = RegionWorker()
        return make_response(success(worker.get(**kwargs)))

    @use_args(RegionSchema(), location="json")
    def post(self, *args):
        try:
            worker = RegionWorker()
            return make_response(success(worker.post(args[0])))
        except ValidationError as e:
            raise e
        except Exception as e:
            logger.error("Error during creation", e)
            raise e

    @use_args({'id': fields.Int(required=True)}, location="query")
    @use_args(RegionSchema(), location="json")
    def put(self, id, *args):
        try:
            worker = RegionWorker()
            return make_response(success(worker.put(id, args[0])))
        except ValidationError as e:
            raise e
        except Exception as err:
            logger.error("Error during update", err)
            raise err

    @use_args({'id': fields.Int(required=True)}, location="query")
    def delete(self, id):
        try:
            worker = RegionWorker()
            worker.delete(id)
            return make_response(success(True))
        except Exception as err:
            logger.error("Error during deletion of region {id}", err)
            raise err
        

