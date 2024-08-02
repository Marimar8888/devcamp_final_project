from flask import Blueprint

# Crear un blueprint principal
bp = Blueprint('main_routes', __name__)

# Importar y registrar el blueprint específico para Guide y user
from .routes_guides import bp as guides_bp
from .routes_users import bp as users_bp

# Registrar los blueprints con un prefijo de URL
bp.register_blueprint(guides_bp)
bp.register_blueprint(users_bp) 