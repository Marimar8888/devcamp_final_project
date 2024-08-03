from app import db, ma

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=False)
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(16), unique=False)

    def __init__(self, name, email, password):
        self.name = name
        self.email = email
        self.password = password
    
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User