import redis
from flask import current_app
from flask.views import MethodView
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt,
    get_jwt_identity,
    jwt_required,
)
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha512
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db
from app.models import UserModel
from app.schemas import UserLoginSchema, UserRegistrationSchema, UserSchema

bp = Blueprint(
    "Auth", __name__, description="Auth operations", url_prefix="/auth"
)


@bp.route("/register")
class UserRegister(MethodView):
    @bp.arguments(UserRegistrationSchema)
    @bp.response(201, UserSchema)
    def post(self, user_data):
        if UserModel.query.filter(
            UserModel.email == user_data["email"]
        ).first():
            abort(409, message="Email already exists.")

        user = UserModel(
            email=user_data["email"],
            password=pbkdf2_sha512.hash(user_data["password"]),
            display_name=user_data.get("display_name", None),
            preferred_language_code=user_data.get(
                "preferred_language_code", "es"
            ),
        )

        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Our engineering monkeys are having trouble")

        return user


@bp.route("/login")
class UserLogin(MethodView):
    @bp.arguments(UserLoginSchema)
    def post(self, user_data):
        user = UserModel.query.filter(
            UserModel.email == user_data["email"]
        ).first()

        if user and pbkdf2_sha512.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(identity=user.id)
            return {
                "access_token": access_token,
                "refresh_token": refresh_token,
            }

        abort(401, message="You shall not pass.")


@bp.route("/logout")
class UserLogout(MethodView):
    def __init__(self):
        self.redis_client = redis.from_url(current_app.config["REDIS_URI"])

    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        self.redis_client.sadd("jwt:blocklist", jti)

        return {"message": "Successfully logged out."}


@bp.route("/refresh")
class TokenRefresh(MethodView):
    def __init__(self):
        self.redis_client = redis.from_url(current_app.config["REDIS_URI"])

    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)

        # Para refrescar el token una vez y poner el refresh token bloqueado
        jti = get_jwt()["jti"]
        self.redis_client.sadd("jwt:blocklist", jti)

        return {"access_token": new_token}
