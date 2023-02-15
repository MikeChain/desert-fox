from marshmallow import fields

from .accounts import AccountSchema, UpdateAccountSchema
from .categories import CategoriesSchema, UpdateCategoriesSchema
from .subcategories import PlainSubcategoriesSchema
from .transactions import TransactionSchema, TransactionUpdateSchema
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
