from flask import Blueprint, request, jsonify
from services.productos_services import (
    obtener_todos, obtener_por_id, crear_producto,
    actualizar_producto, eliminar_producto
)

productos_bp = Blueprint('productos', __name__)

@productos_bp.route('/', methods=['GET'])
def home():
    return 'Bienvenido a la API de productos'

@productos_bp.route('/productos', methods=['GET'])
def obtener_productos():
    return obtener_todos()

@productos_bp.route('/productos/<int:id>', methods=['GET'])
def obtener_producto(id):
    return obtener_por_id(id)

@productos_bp.route('/productos', methods=['POST'])
def agregar_producto():
    return crear_producto(request.json)

@productos_bp.route('/productos/<int:id>', methods=['PUT'])
def actualizar_producto_route(id):
    return actualizar_producto(id, request.json)

@productos_bp.route('/productos/<int:id>', methods=['DELETE'])
def eliminar_producto_route(id):
    return eliminar_producto(id)