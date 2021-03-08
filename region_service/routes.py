from flask import jsonify, request, make_response
from flask_restful import Resource
from .model.region import RegionSchema, region_args
from .workers.region_worker import RegionWorker
from webargs.flaskparser import use_kwargs, use_args
from .utils import *
from flask import request
from . import db
from marshmallow import ValidationError
import traceback

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
        except ValidationError as err:
            raise e
        # except Exception as e:
        #     return make_response(error("Error creating region"))