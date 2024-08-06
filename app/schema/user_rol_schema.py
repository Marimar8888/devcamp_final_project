from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models import UserRol

class UserRolSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = UserRol
        load_instance = True
        include_fk = True

