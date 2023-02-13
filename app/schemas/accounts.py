from marshmallow import Schema, fields, validate


class AccountSchema(Schema):
    id = fields.UUID(dump_only=True)
    name = fields.String(required=True)
    account_type = fields.String(
        validate=validate.OneOf(["cash", "debit", "credit"]), required=True
    )
    currency = fields.String(
        validate=validate.OneOf(["MXN", "USD", "EUR"]), required=True
    )
    initial_balance = fields.Decimal()


class UpdateAccountSchema(Schema):
    name = fields.String()
    account_type = fields.String(
        validate=validate.OneOf(["cash", "debit", "credit"])
    )
    currency = fields.String(validate=validate.OneOf(["MXN", "USD", "EUR"]))
    initial_balance = fields.Decimal()
