from marshmallow import Schema, fields, validate


class UserRegistrationSchema(Schema):
    email = fields.Email(attribute="email", required=True)
    password = fields.String(required=True)
    display_name = fields.String()
    preferred_language_code = fields.String(
        validate=validate.OneOf(["es", "en"])
    )


class UserLoginSchema(Schema):
    email = fields.Email(attribute="email", required=True)
    password = fields.String(required=True)


class UserSchema(Schema):
    id = fields.UUID(required=True)
    email = fields.Email(attribute="email", required=True)
    display_name = fields.String()
    preferred_language_code = fields.String(
        required=True, validate=validate.OneOf(["es", "en"])
    )


class UserUpdateSchema(Schema):
    email = fields.Email(attribute="email")
    display_name = fields.String()
    preferred_language_code = fields.String(
        validate=validate.OneOf(["es", "en"])
    )
    password = fields.String()
