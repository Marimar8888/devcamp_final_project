from flask import Blueprint

# Crear un blueprint principal
bp = Blueprint('main_routes', __name__)

# Importar y registrar el blueprint específico 

from .routes_users import bp as users_bp
from .routes_courses import bp as courses_bp
from .routes_study_centers import bp as studyCenters_bp
from .routes_professors import bp as professors_bp
from .routes_students import bp as students_bp
from .routes_categories import bp as categories_bp
from .routes_professor_studycenter import bp as professor_studycenter_bp
from .routes_rols import bp as rols_bp
from .routes_user_rol import bp as user_rol_bp
from .routes_enrollments import bp as enrollments_bp
from .routes_studycenter_student import bp as studycenter_student_bp
from .routes_favorites import bp as favorites_bp

# Registrar los blueprints sin prefijo de URL

bp.register_blueprint(users_bp) 
bp.register_blueprint(courses_bp) 
bp.register_blueprint(studyCenters_bp) 
bp.register_blueprint(professors_bp) 
bp.register_blueprint(students_bp) 
bp.register_blueprint(categories_bp)
bp.register_blueprint(professor_studycenter_bp)
bp.register_blueprint(rols_bp) 
bp.register_blueprint(user_rol_bp) 
bp.register_blueprint(enrollments_bp)
bp.register_blueprint(studycenter_student_bp)
bp.register_blueprint(favorites_bp)

