from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.rol import Rol

class RolSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Rol
        load_instance = True