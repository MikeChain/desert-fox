import redis
from flask import current_app, request
from flask.views import MethodView
from flask_jwt_extended import (
    create_access_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)
from flask_smorest import Blueprint, abort

from app.exceptions import (
    AlreadyExistsError,
    AuthenticationFailedException,
    DatabaseError,
    UserNotFoundException,
)
from app.schemas import UserLoginSchema, UserRegistrationSchema, UserSchema
from app.services.user import UserService

bp = Blueprint(
    "Auth", __name__, description="Auth operations", url_prefix="/v1/auth"
)


@bp.route("/register")
class UserRegister(MethodView):
    @bp.arguments(UserRegistrationSchema)
    @bp.response(201, UserSchema)
    def post(self, user_data):
        try:
            user = UserService().create_user(user_data)
        except AlreadyExistsError:
            abort(409, message="Email already exists.")
        except DatabaseError:
            abort(500, message="Our engineering monkeys are having trouble")

        return user


@bp.route("/login")
class UserLogin(MethodView):
    @bp.arguments(UserLoginSchema)
    def post(self, user_data):
        try:
            user_tokens = UserService().authenticate(
                user_data["email"], user_data["password"]
            )

            return user_tokens
        except UserNotFoundException:
            abort(404, message="User not found.")
        except AuthenticationFailedException:
            abort(401, message="You shall not pass.")


@bp.route("/logout")
class UserLogout(MethodView):
    def __init__(self):
        self.redis_client = redis.from_url(current_app.config["REDIS_URI"])

    @jwt_required()
    def post(self):
        self.redis_client.sadd("jwt:blocklist", get_jwt()["jti"])
        self.redis_client.sadd("jwt:blocklist", get_jwt()["r_jti"])

        return {"message": "Successfully logged out."}


@bp.route("/refresh")
class TokenRefresh(MethodView):
    def __init__(self):
        self.redis_client = redis.from_url(current_app.config["REDIS_URI"])

    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        claims = get_jwt()
        jti = claims["jti"]
        additional_claims = {
            "u_type": claims["u_type"],
            "lang": claims["lang"],
            "r_jti": jti,
        }
        new_token = create_access_token(
            identity=current_user,
            additional_claims=additional_claims,
            fresh=False,
        )

        # Para refrescar el token una vez y poner el refresh token bloqueado
        self.redis_client.sadd("jwt:blocklist", jti)

        return {"access_token": new_token}
