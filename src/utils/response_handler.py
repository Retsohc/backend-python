from flask import jsonify

def success_response(data=None, message='Operación exitosa', status_code=200):
    response = {'success': True, 'message': message}
    if data is not None:
        response['data'] = data
    return jsonify(response), status_code

def error_response(message='Ocurrió un error', status_code=500, details=None):
    response = {'success': False, 'message': message}
    if details:
        response['details'] = str(details)
    return jsonify(response), status_code

def not_found_response(message='Recurso no encontrado'):
    return error_response(message, 404)

def bad_request_response(message='Solicitud inválida'):
    return error_response(message, 400)