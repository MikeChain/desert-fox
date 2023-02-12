from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha512
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db
from app.models import UserModel
from app.schemas import UserSchema, UserUpdateSchema
from app.services import UserService

bp = Blueprint(
    "Users", __name__, description="Operations on users", url_prefix="/users"
)


@bp.route("/")
class UsersList(MethodView):
    @bp.response(200, UserSchema(many=True))
    def get(self):
        return UserService.get_all_users()


@bp.route("/<uuid:user_id>")
class User(MethodView):
    @bp.response(200, UserSchema)
    def get(self, user_id):
        return UserService.get_user_404(user_id)

    @bp.arguments(UserUpdateSchema)
    @bp.response(200, UserSchema)
    def put(self, user_data, user_id):
        user = UserService.get_user_404(user_id)

        user.display_name = user_data.get("display_name", user.display_name)
        user.email = user_data.get("email", user.email)
        user.preferred_language_code = user_data.get(
            "preferred_language_code", user.preferred_language_code
        )

        if "password" in user_data:
            user.password = pbkdf2_sha512.hash(user_data["password"])

        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="Our engineering monkeys are having trouble")

        return user
