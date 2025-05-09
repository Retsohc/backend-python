from src.database.db import get_connection
from src.utils.response_handler import success_response, error_response, bad_request_response

def guardar_producto_externo(data):
    required_fields = ['title', 'price', 'description', 'category']
    if not all(field in data for field in required_fields):
        return bad_request_response('Campos incompletos para guardar el producto externo')

    query = 'INSERT INTO productos (title, price, description, category) VALUES (%s, %s, %s, %s)'
    conn = get_connection()

    if conn is None:
        return error_response('Error en la conexión a la base de datos')
    cursor = conn.cursor()
    try:
        cursor.execute(query, (data['title'], data['price'], data['description'], data['category']))
        conn.commit()
        return success_response({'id': cursor.lastrowid}, 'Producto externo guardado correctamente', 201)
    except Exception as e:
        return error_response('Error al guardar el producto externo', details=str(e))
    finally:
        cursor.close()
        conn.close()
        return None