import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='productos_db'
        )
        if connection.is_connected():
            print("Conectado a la base de datos MySQL")
            return connection
    except Error as e:
        print(f"Error conectando a la base de datos: {e}")
        return None