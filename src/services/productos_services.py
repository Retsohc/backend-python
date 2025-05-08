from flask import Blueprint, request
from src.database.db import get_connection
from src.utils.response_handler import (
    success_response,
    error_response,
    not_found_response,
    bad_request_response
)

productos_bp = Blueprint('productos', __name__)

def execute_query(query, params=None, fetchone=False):
    conn = get_connection()
    if conn is None:
        return None, error_response('Error en la conexión a la base de datos')
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute(query, params or ())
        if fetchone:
            return cursor.fetchone(), None
        return cursor.fetchall(), None
    except Exception as e:
        return None, error_response('Error al ejecutar la consulta', details=str(e))
    finally:
        cursor.close()
        conn.close()

@productos_bp.route('/', methods=['GET'])
def home():
    return success_response(message='Bienvenido a la API de productos')

@productos_bp.route('/productos', methods=['GET'])
def obtener_productos():
    query = 'SELECT * FROM productos'
    productos, error = execute_query(query)
    if error:
        return error
    if not productos:
        return success_response([], message='No hay productos disponibles')
    return success_response(productos)

@productos_bp.route('/productos/<int:id>', methods=['GET'])
def obtener_producto(id):
    query = 'SELECT * FROM productos WHERE id = %s'
    producto, error = execute_query(query, (id,), fetchone=True)
    if error:
        return error
    if producto:
        return success_response(producto)
    return not_found_response('Producto no encontrado')

@productos_bp.route('/productos', methods=['POST'])
def agregar_producto():
    data = request.json
    required_fields = ['title', 'price', 'description', 'category']
    if not all(field in data for field in required_fields):
        return bad_request_response('Todos los campos son obligatorios')

    query = 'INSERT INTO productos (title, price, description, category) VALUES (%s, %s, %s, %s)'
    conn = get_connection()

    if conn is None:
        return error_response('Error en la conexión a la base de datos')
    cursor = conn.cursor()
    try:
        cursor.execute(query, (data['title'], data['price'], data['description'], data['category']))
        conn.commit()
        return success_response({'id': cursor.lastrowid}, 'Producto agregado correctamente', 201)
    except Exception as e:
        return error_response('Error al agregar el producto', details=str(e))
    finally:
        cursor.close()
        conn.close()

@productos_bp.route('/productos/<int:id>', methods=['PUT'])
def actualizar_producto(id):
    data = request.json
    required_fields = ['title', 'price', 'description', 'category']
    if not all(field in data for field in required_fields):
        return bad_request_response('Todos los campos son obligatorios')
    
    query = '''
    UPDATE productos 
    SET title = %s, price = %s, description = %s, category = %s
    WHERE id = %s
    '''
    conn = get_connection()
    if conn is None:
        return error_response('Error en la conexión a la base de datos')
    cursor = conn.cursor()
    try:
        cursor.execute(query, (
            data['title'], data['price'], data['description'],
            data['category'], id
        ))
        conn.commit()
        return success_response(message='Producto actualizado correctamente')
    except Exception as e:
        return error_response('Error al actualizar el producto', details=str(e))
    finally:
        cursor.close()
        conn.close()

@productos_bp.route('/productos/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    query = 'DELETE FROM productos WHERE id = %s'
    conn = get_connection()
    if conn is None:
        return error_response('Error en la conexión a la base de datos')
    cursor = conn.cursor()
    try:
        cursor.execute(query, (id,))
        conn.commit()
        return '', 204
    except Exception as e:
        return error_response('Error al eliminar el producto', details=str(e))
    finally:
        cursor.close()
        conn.close()