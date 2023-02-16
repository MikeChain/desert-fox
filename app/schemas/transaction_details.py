from marshmallow import Schema, fields, validate


class PlainTransactionDetailsSchema(Schema):
    id = fields.UUID(dump_only=True)
    subcategory_id = fields.UUID(required=True)
    description = fields.String(required=True)
    amount = fields.Number(required=True)


class PlainTransactionDetailsUpdateSchema(Schema):
    subcategory_id = fields.UUID()
    description = fields.String()
    amount = fields.Number()