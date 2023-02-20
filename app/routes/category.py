from flask.views import MethodView
from flask_jwt_extended import get_jwt, jwt_required
from flask_smorest import Blueprint, abort

from app.exceptions import AlreadyExistsError, DatabaseError, ResourceInUseError
from app.schemas import CategoriesSchema, UpdateCategoriesSchema
from app.services import CategoriesService

bp = Blueprint(
    "Category",
    __name__,
    description="Operations on categories",
    url_prefix="/api/v1/categories",
)


@bp.route("")
class Category(MethodView):
    @jwt_required()
    @bp.response(200, CategoriesSchema(many=True))
    def get(self):
        return CategoriesService().get_all_categories()

    @jwt_required(fresh=True)
    @bp.arguments(CategoriesSchema)
    @bp.response(201, CategoriesSchema)
    def post(self, category_data):
        claims = get_jwt()
        u_type = claims["u_type"]

        if u_type != "admin":
            abort(401, message="You shall not pass.")

        try:
            category = CategoriesService().create_category(category_data)
        except AlreadyExistsError:
            abort(409, message="Category already exists.")
        except DatabaseError:
            abort(500, message="Our engineering monkeys are having trouble")

        return category


@bp.route("/<uuid:category_id>")
class SingleCategory(MethodView):
    @jwt_required()
    @bp.response(200, CategoriesSchema)
    def get(self, category_id):
        return CategoriesService().get_category(category_id)

    @jwt_required(fresh=True)
    @bp.arguments(UpdateCategoriesSchema)
    @bp.response(201, CategoriesSchema)
    def put(self, category_data, category_id):
        claims = get_jwt()
        u_type = claims["u_type"]

        if u_type != "admin":
            abort(401, message="You shall not pass.")

        try:
            category = CategoriesService().update_category(
                category_data, category_id
            )
        except AlreadyExistsError:
            abort(409, message="Category already exists.")

        return category

    @jwt_required(fresh=True)
    def delete(self, category_id):
        claims = get_jwt()
        u_type = claims["u_type"]

        if u_type != "admin":
            abort(
                401,
                message="Nice try, slick. But you're not getting in without proper authorization.",
            )

        try:
            CategoriesService().delete_category(category_id)
        except ResourceInUseError:
            abort(
                400,
                message="The fault, dear user, is not in our server, but in ourselves, that we attempt to delete a referenced category.",
            )
        except DatabaseError:
            abort(
                500,
                message="Good news, everyone! Our servers are experiencing technical difficulties.",
            )

        return {"message": "Category deleted!"}
