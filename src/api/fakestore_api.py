import requests

BASE_URL = 'https://fakestoreapi.com'

def obtener_producto_externos():
    try:
        response = requests.get(f'{BASE_URL}/products')
        response.raise_for_status()
        productos = response.json()
        return productos[:20], None
    except requests.RequestException as e:
        return None, str(e)

def obtener_producto_externo_por_id(id):
    try:
        response = requests.get(f'{BASE_URL}/products/{id}')
        response.raise_for_status()
        return response.json(), None
    except requests.RequestException as e:
        return None, str(e)