import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')  # Usa el valor de SECRET_KEY del archivo .env
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')  # Usa el valor de DATABASE_URL del archivo .env
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = os.path.abspath(os.getenv('UPLOAD_FOLDER', 'static/uploads'))
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # Limite de tamaño de archivo (16 MB)
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}  # Extensiones permitidas

    @staticmethod
    def allowed_file(filename):
        """Verifica si el archivo tiene una extensión permitida."""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS
