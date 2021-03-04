from flask import jsonify

def success(data):
    return jsonify({
        'status': 'success',
        'data': data
    }), 200

def error(message):
    return jsonify({
        'status': 'error',
        'message': message
    }), 500