from flask import Blueprint, jsonify
from src.api.fakestore_api import obtener_producto_externo_por_id, obtener_producto_externos
from src.services.productos_services import guardar_producto_externo
from src.utils.response_handler import error_response

productos_bp = Blueprint('productos_bp', __name__)

@productos_bp.route('/productos-externos', methods=['GET'])
def obtener_producto_externos():
    producto, error = obtener_producto_externos()
    if error:
        return jsonify({'success': False, 'message': 'Error al obtener productos externos', 'details': error}), 500
    return jsonify({'success': True, 'data': producto})

@productos_bp.route('/productos-externos/<int:id>', methods=['GET'])
def obtener_producto_externo(id):
    producto, error = obtener_producto_externo_por_id(id)
    if error:
        return jsonify({'success': False, 'message': 'Error al obtener producto externo', 'details': error}), 500
    return jsonify({'success': True, 'data': producto})

@productos_bp.route('/productos-externos/<int:id>/guardar', methods=['POST'])
def guardar_producto_externo_route(id):
    producto, error = obtener_producto_externo_por_id(id)
    if error:
        return error_response('Error al obtener el producto externo', details=error)
    return guardar_producto_externo(producto)