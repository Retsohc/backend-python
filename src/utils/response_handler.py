from flask import jsonify

def success_response(data=None, message='Operación exitosa', status_code=200):
    response = {
        'success': True,
        'message': message,
        'data': data
    }
    return jsonify(response), status_code

def error_response(message='Error interno del servidor', details=None, status_code=500):
    response = {
        'success': False,
        'message': message,
        'details': details
    }
    return jsonify(response), status_code

def bad_request_response(message='Solicitud incorrecta', details=None):
    return error_response(message=message, details=details, status_code=400)