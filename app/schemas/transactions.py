from marshmallow import Schema, fields


class TransactionSchema(Schema):
    id = fields.UUID(dump_only=True)
    type = fields.String(required=True)
    status = fields.String(required=True)
    total_amount = fields.Number(required=True)
    transaction_date = fields.DateTime(required=True)
    notes = fields.String()


class TransactionUpdateSchema(Schema):
    type = fields.String()
    status = fields.String()
    total_amount = fields.Number()
    transaction_date = fields.DateTime()
    notes = fields.String()
