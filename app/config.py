import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')  # Usa el valor de SECRET_KEY del archivo .env
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')  # Usa el valor de DATABASE_URL del archivo .env
    SQLALCHEMY_TRACK_MODIFICATIONS = False
