from flask import Blueprint, jsonify, request
from .model.region import Region, RegionSchema
from flask import request
from . import db

regions = Blueprint('regions', __name__)


@regions.route('/')
def get_regions():
    all_regions = Region.all()
    return 


@regions.route('/', methods=['POST'])
def add_region():
    json_request = request.get_json()
    if not json_request['description']:
        return jsonify({
            'status': 'fail',
            'message': 'The description is a mandatory field'
        }), 400
    
    
    