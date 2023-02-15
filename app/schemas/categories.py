from marshmallow import Schema, fields, validate

from .subcategories import PlainSubcategoriesSchema


class CategoriesSchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.String(required=True)
    description = fields.String(required=True)
    type = fields.String(
        validate=validate.OneOf(["income", "expense"]), required=True
    )


class UpdateCategoriesSchema(Schema):
    name = fields.String()
    description = fields.String()
