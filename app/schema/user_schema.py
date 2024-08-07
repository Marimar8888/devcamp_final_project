from marshmallow import Schema, fields

class RolSchema(Schema):
    rols_id = fields.Int()
    rols_name = fields.Str()

class UserSchema(Schema):
    users_id = fields.Int()
    users_name = fields.Str()
    users_email = fields.Str()
    users_password = fields.Str()
    rols = fields.List(fields.Nested(RolSchema))

class LoginUserSchema(Schema):
    users_id = fields.Int()
    users_name = fields.Str()
    users_email = fields.Str()
    users_password = fields.Str()