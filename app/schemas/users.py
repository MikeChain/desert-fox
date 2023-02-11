from marshmallow import Schema, fields


class UserRegistrationSchema(Schema):
    email = fields.Email(attribute="email", required=True)
    password = fields.String(required=True)
    display_name = fields.String()
    preferred_language_code = fields.String(required=True)


class UserLoginSchema(Schema):
    email = fields.String(required=True)
    password = fields.String(required=True)


class UserSchema(Schema):
    id = fields.UUID(required=True)
    email = fields.String(required=True)
    display_name = fields.String()
    preferred_language_code = fields.String(required=True)


class UserUpdateSchema(Schema):
    email = fields.String()
    display_name = fields.String()
    preferred_language_code = fields.String()
    password = fields.String()
