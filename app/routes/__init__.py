from flask import Blueprint

# Crear un blueprint principal
bp = Blueprint('main_routes', __name__)

# Importar y registrar el blueprint específico 

from .routes_users import bp as users_bp
from .routes_courses import bp as courses_bp
from .routes_study_centers import bp as studyCenters_bp
from .routes_professors import bp as professors_bp
from .routes_professor_studycenter import bp as professor_studycenter_bp

# Registrar los blueprints sin prefijo de URL

bp.register_blueprint(users_bp) 
bp.register_blueprint(courses_bp) 
bp.register_blueprint(studyCenters_bp) 
bp.register_blueprint(professors_bp) 
bp.register_blueprint(professor_studycenter_bp)
