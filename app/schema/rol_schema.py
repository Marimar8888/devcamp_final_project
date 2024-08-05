from app import ma
from app.models.rol import Rol

class RolSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Rol
        load_instance = True