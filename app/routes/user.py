from flask.views import MethodView
from flask_jwt_extended import get_jwt, jwt_required
from flask_smorest import Blueprint, abort

from app.exceptions import DatabaseError
from app.schemas import UserSchema, UserUpdateSchema
from app.services import UserService

bp = Blueprint(
    "Users",
    __name__,
    description="Operations on users",
    url_prefix="/api/v1/users",
)


@bp.route("")
class UsersList(MethodView):
    @jwt_required(fresh=True)
    @bp.response(200, UserSchema(many=True))
    def get(self):
        claims = get_jwt()
        if claims["u_type"] != "admin":
            abort(401, message="You shall not pass.")
        return UserService().get_all_users()


@bp.route("/<uuid:user_id>")
class User(MethodView):
    @jwt_required()
    @bp.response(200, UserSchema)
    def get(self, user_id):
        return UserService().get_user_404(user_id)

    @jwt_required(fresh=True)
    @bp.arguments(UserUpdateSchema)
    @bp.response(200, UserSchema)
    def put(self, user_data, user_id):
        try:
            user = UserService().update(user_data, user_id)
        except DatabaseError:
            abort(500, message="Our engineering monkeys are having trouble")

        return user
