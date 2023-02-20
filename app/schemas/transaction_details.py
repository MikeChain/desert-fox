from marshmallow import Schema, fields, validate


class PlainTransactionDetailsSchema(Schema):
    id = fields.UUID(dump_only=True)
    subcategory_id = fields.UUID(required=True)
    description = fields.String(required=True)
    amount = fields.Number(required=True)


class PlainTransactionDetailsUpdateSchema(Schema):
    id = fields.UUID(required=True)
    subcategory_id = fields.UUID()
    description = fields.String()
    amount = fields.Number()


class PaymentAccountsSchema(Schema):
    account_id = fields.UUID(load_only=True)
    subtotal_amount = fields.Number(required=True)
    type = fields.String(load_only=True)


class PaymentUpdateSchema(Schema):
    id = fields.UUID(required=True)
    subtotal_amount = fields.Number(required=True)


class DetailsSchema(Schema):
    accounts = fields.List(fields.Nested(PaymentUpdateSchema))
    transaction_details = fields.List(
        fields.Nested(PlainTransactionDetailsUpdateSchema)
    )
