from marshmallow import Schema, fields, validate


class PlainTransactionSchema(Schema):
    id = fields.UUID(dump_only=True)
    type = fields.String(
        required=True, validate=validate.OneOf(["income", "expense"])
    )
    status = fields.String(
        dump_only=True,
        validate=validate.OneOf(["pending", "verified", "rejected"]),
    )
    total_amount = fields.Number(dump_only=True)
    transaction_date = fields.DateTime(required=True)
    notes = fields.String()


class PlainTransactionUpdateSchema(Schema):
    type = fields.String(validate=validate.OneOf(["income", "expense"]))
    status = fields.String(
        validate=validate.OneOf(["pending", "verified", "rejected"])
    )
    transaction_date = fields.DateTime()
    notes = fields.String()
