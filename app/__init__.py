from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from app.config import Config
import os

# Inicializar extensiones
db = SQLAlchemy()
ma = Marshmallow()

def create_app():
    app = Flask(__name__)

    # Configurar CORS para permitir solicitudes desde http://localhost:3000
    CORS(app, resources={
        r"/*": {
            "origins": "http://localhost:3000",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "headers": ["Content-Type", "Authorization"]
        }
    })

    # Cargar configuración desde el objeto Config
    app.config.from_object(Config)
    
    # Inicializar extensiones con la aplicación
    db.init_app(app)
    ma.init_app(app)

    # Configurar la carpeta de subida y el tamaño máximo de contenido
    app.config['UPLOAD_FOLDER'] = Config.UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = Config.MAX_CONTENT_LENGTH
    
    # Registrar Blueprints
    from app.routes import bp
    app.register_blueprint(bp)
    
    return app
