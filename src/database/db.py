import mysql.connector

def get_connection():
    try:
        return mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='db_products'
        )
    except mysql.connector.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None
