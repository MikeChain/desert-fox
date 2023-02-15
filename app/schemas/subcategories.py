from marshmallow import Schema, fields


class PlainSubcategoriesSchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.String(required=True)
