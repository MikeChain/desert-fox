from .auth import bp as AuthBp
from .user import bp as UserBp

BPS_TO_IMPORT = (
    AuthBp,
    UserBp,
)
