from flask import Flask
from flask_cors import CORS
from src.routes.productos_routes import productos_bp

app = Flask(__name__)
CORS(app, resources={r"/productos*": {"origins": "http://localhost:4200"}})

app.register_blueprint(productos_bp)

if __name__ == '__main__':
    app.run(port=3000, debug=True)