from flask import Blueprint, jsonify, request
from .model.region import Region
from flask import request
from . import db

regions = Blueprint('regions', __name__)

@regions.route('/')
def get_regions():
    all_regions = Region.query.all()
    return jsonify({
        'status': 'success',
        'data': {
            'regions': [jsonify(region) for region in all_regions]
        }
    })


@regions.route('/', methods=['POST'])
def add_region():
    json_request = request.get_json()
    if not json_request['description']:
        return jsonify({
            'status': 'fail',
            'message': 'The description is a mandatory field'
        }), 400
    