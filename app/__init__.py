from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Inicializar extensiones
db = SQLAlchemy()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)
    
    # Cargar configuración
    app.config.from_object('app.config.Config')
    
    # Inicializar extensiones
    db.init_app(app)
    ma.init_app(app)
    
    # Registrar Blueprints
    from app.routes import bp
    app.register_blueprint(bp)
    
    return app
