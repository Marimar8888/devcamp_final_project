from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os

# Inicializar extensiones
db = SQLAlchemy()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    # Cargar configuración
    app.config.from_object('app.config.Config')
    
    # Inicializar extensiones
    db.init_app(app)
    ma.init_app(app)

    CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
    
    # Registrar Blueprints
    from app.routes import bp
    app.register_blueprint(bp)
    
    return app
