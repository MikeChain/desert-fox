from .accounts import bp as AccountsBp
from .auth import bp as AuthBp
from .category import bp as CategoryBp
from .subcategory import bp as SubcategoryBp
from .user import bp as UserBp

BPS_TO_IMPORT = (
    AccountsBp,
    AuthBp,
    CategoryBp,
    SubcategoryBp,
    UserBp,
)
