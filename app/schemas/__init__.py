from marshmallow import fields

from .accounts import AccountSchema, SimpleAccountSchema, UpdateAccountSchema
from .categories import CategoriesSchema, UpdateCategoriesSchema
from .subcategories import PlainSubcategoriesSchema
from .transaction_details import (
    PaymentAccountsSchema,
    PlainTransactionDetailsSchema,
    PlainTransactionDetailsUpdateSchema,
)
from .transactions import PlainTransactionSchema, PlainTransactionUpdateSchema
from .users import (
    UserLoginSchema,
    UserRegistrationSchema,
    UserSchema,
    UserUpdateSchema,
)


class SubcategoriesSchema(PlainSubcategoriesSchema):
    category_id = fields.UUID(required=True, load_only=True)
    category = fields.Nested(CategoriesSchema(), dump_only=True)


class CategoriesWithSubSchema(CategoriesSchema):
    subcategories = fields.List(
        fields.Nested(PlainSubcategoriesSchema()), dump_only=True
    )


class AccountData(PaymentAccountsSchema):
    accounts = fields.Nested(SimpleAccountSchema, dump_only=True)


class TransactionSchema(PlainTransactionSchema):
    transaction_details = fields.List(
        fields.Nested(PlainTransactionDetailsSchema)
    )
    accounts = fields.List(fields.Nested(AccountData))
