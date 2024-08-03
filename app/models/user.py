from app import db, ma

class User(db.Model):
    __tablename__ = 'users'
    users_id = db.Column(db.Integer, primary_key=True)
    users_name = db.Column(db.String(100), unique=False, nullable=True)
    users_email = db.Column(db.String(80), unique=True, nullable=True)
    users_password = db.Column(db.String(16), unique=False, nullable=True)

    def __init__(self, users_name, users_email, users_password):
        self.users_name = users_name
        self.users_email = users_email
        self.users_password = users_password
    
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User