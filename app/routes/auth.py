from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha512
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db
from app.models import UserModel
from app.schemas import UserRegistrationSchema, UserSchema

bp = Blueprint(
    "Auth", __name__, description="Auth operations", url_prefix="/auth"
)


@bp.route("/register")
class UserRegister(MethodView):
    @bp.arguments(UserRegistrationSchema)
    @bp.response(200, UserSchema)
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
    def post():
        pass


@bp.route("/logout")
class UserLogout(MethodView):
    def post():
        pass


@bp.route("/refresh")
class TokenRefresh(MethodView):
    def post():
        pass
