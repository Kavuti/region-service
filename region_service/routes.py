from flask import Blueprint, jsonify, request
from .model.region import Region, RegionSchema
from flask import request
from . import db
import logging

regions = Blueprint('regions', __name__)
logger = logging.getLogger()

@regions.route('/')
def get_regions():
    all_regions = Region.query.all()
    return jsonify(RegionSchema(many=True).dump(all_regions))


@regions.route('/', methods=['POST'])
def add_region():
    json_request = request.get_json()
    if not json_request['description']:
        return jsonify({
            'status': 'fail',
            'message': 'The description is a mandatory field'
        }), 400
    
    try:
        logger.info(json_request)
        schema = RegionSchema()
        new_region = schema.load(json_request, transient=True)
        db.session.add(new_region)
        db.session.commit()
        return jsonify({
            'status': 'success',
            'data': jsonify(schema.load(new_region))
        }), 200
    except Exception as e:
        logger.error("Error saving new region", e)
        db.session.rollback()
        return jsonify({
            'status': 'error',
            'message': 'Error saving a new region'
        }), 500
    
    