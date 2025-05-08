from flask import Blueprint, request
from src.database.db import get_connection
from src.utils.response_handler import ( success_response,
    error_response,
    not_found_response,
    bad_request_response
)

productos_bp = Blueprint('productos', __name__)

@productos_bp.route('/', methods=['GET'])
def home():
    return success_response(message='Bienvenido a la API de productos')

@productos_bp.route('/productos', methods=['GET'])
def obtener_productos():
    conn = get_connection()
    if conn is None:
        return error_response('Error en la conexión a la base de datos')
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute('SELECT * FROM productos')
        productos = cursor.fetchall()
        return success_response(productos)
    except Exception as e:
        return error_response('Error al obtener los productos', details=e)
    finally:
        cursor.close()
        conn.close()

@productos_bp.route('/productos/<int:id>', methods=['GET'])
def obtener_producto(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute('SELECT * FROM productos WHERE id = %s', (id,))
        producto = cursor.fetchone()
        if producto:
            return success_response(producto)
        return not_found_response('Producto no encontrado')
    except Exception as e:
        return error_response('Error al obtener el producto', details=e)
    finally:
        cursor.close()
        conn.close()

@productos_bp.route('/productos', methods=['POST'])
def agregar_producto():
    data = request.json
    required_fields = ['title', 'price', 'description', 'category', 'image']
    if not all(field in data for field in required_fields):
        return bad_request_response('Todos los campos son obligatorios')

    conn = get_connection()
    cursor = conn.cursor()
    try:
        sql = 'INSERT INTO productos (title, price, description, category, image) VALUES (%s, %s, %s, %s, %s)'
        cursor.execute(sql, (data['title'], data['price'], data['description'], data['category'], data['image']))
        conn.commit()
        return success_response({'id': cursor.lastrowid}, 'Producto agregado correctamente', 201)
    except Exception as e:
        return error_response('Error al agregar el producto', details=e)
    finally:
        cursor.close()
        conn.close()

@productos_bp.route('/productos/<int:id>', methods=['PUT'])
def actualizar_producto(id):
    data = request.json
    conn = get_connection()
    cursor = conn.cursor()
    try:
        sql = '''
        UPDATE productos 
        SET title = %s, price = %s, description = %s, category = %s, image = %s 
        WHERE id = %s
        '''
        cursor.execute(sql, (
            data['title'], data['price'], data['description'],
            data['category'], data['image'], id
        ))
        conn.commit()
        return success_response(message='Producto actualizado correctamente')
    except Exception as e:
        return error_response('Error al actualizar el producto', details=e)
    finally:
        cursor.close()
        conn.close()

@productos_bp.route('/productos/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM productos WHERE id = %s', (id,))
        conn.commit()
        return success_response(message='Producto eliminado correctamente', status_code=204)
    except Exception as e:
        return error_response('Error al eliminar el producto', details=e)
    finally:
        cursor.close()
        conn.close()