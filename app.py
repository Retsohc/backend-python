from flask import Flask
from flask_cors import CORS
from routes.productos_routes import productos_bp

app = Flask(__name__)
CORS(app, resources={r"/productos*": {"origins": "http://localhost:4200"}})

# Rutas registradas
app.register_blueprint(productos_bp)