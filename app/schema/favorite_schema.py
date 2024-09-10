from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models.favorite import Favorite

class FavoriteSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Favorite
        load_instance = True
        include_fk = True

