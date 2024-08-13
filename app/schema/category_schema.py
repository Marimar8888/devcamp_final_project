from app import ma
from app.models.category import Category

class CategorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Category
        include_relationships = True
