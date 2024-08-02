from flask import Blueprint

# Crear un blueprint principal
bp = Blueprint('main_routes', __name__)

# Importar y registrar el blueprint específico para Guide
from .routes_guides import bp as guides_bp

# Registrar los blueprints con un prefijo de URL
bp.register_blueprint(guides_bp)