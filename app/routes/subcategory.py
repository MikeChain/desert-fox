from flask.views import MethodView
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from flask_smorest import Blueprint, abort

from app.exceptions import AlreadyExistsError, DatabaseError
from app.schemas import PlainSubcategoriesSchema, SubcategoriesSchema
from app.services import SubcategoriesService

bp = Blueprint(
    "Subcategory",
    __name__,
    description="Operations on subcategories",
    url_prefix="/v1/subcategories",
)


@bp.route("")
class Subcategory(MethodView):
    @jwt_required()
    @bp.response(200, SubcategoriesSchema(many=True))
    def get(self):
        return SubcategoriesService().get_all_subcategories()

    @jwt_required()
    @bp.arguments(SubcategoriesSchema)
    @bp.response(201, SubcategoriesSchema)
    def post(self, subcategory_data):
        claims = get_jwt()
        u_type = claims["u_type"]

        if u_type not in ("pro", "admin"):
            abort(401, message="You shall not pass.")

        subcategory_data["user_id"] = claims["sub"]

        try:
            subcategory = SubcategoriesService().create_subcategory(
                subcategory_data
            )
        except AlreadyExistsError:
            abort(409, message="Subcategory already exists.")
        except DatabaseError:
            abort(500, message="Our engineering monkeys are having trouble")

        return subcategory


@bp.route("/<uuid:subcategory_id>")
class SingleSubcategory(MethodView):
    @jwt_required()
    @bp.response(200, SubcategoriesSchema)
    def get(self, subcategory_id):
        user_id = get_jwt_identity()
        return SubcategoriesService().get_subcategory(subcategory_id, user_id)
