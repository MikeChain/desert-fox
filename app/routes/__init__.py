from .accounts import bp as AccountsBp
from .auth import bp as AuthBp
from .user import bp as UserBp

BPS_TO_IMPORT = (
    AccountsBp,
    AuthBp,
    UserBp,
)
