from flask import request
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_smorest import Blueprint, abort

from app.exceptions import AlreadyExistsError, DatabaseError, ResourceInUseError
from app.schemas import (
    AccountSchema,
    PaginatedAccountSchema,
    UpdateAccountSchema,
)
from app.services import AccountsService

bp = Blueprint(
    "Accounts",
    __name__,
    description="Operations on accounts",
    url_prefix="/api/v1/accounts",
)


@bp.route("")
class Accounts(MethodView):
    @jwt_required()
    # @bp.response(200, AccountSchema(many=True))
    def get(self):
        page = request.args.get("page", default=1, type=int)
        size = request.args.get("size", default=5, type=int)
        current_user = get_jwt_identity()
        schema = PaginatedAccountSchema()
        pagination = AccountsService().get_pagination(current_user, page, size)
        data = {"page": page, "per_page": size, "pages": pagination.pages}
        schema.load(data)
        return schema.dump(pagination)

    @jwt_required()
    @bp.arguments(AccountSchema)
    @bp.response(201, AccountSchema)
    def post(self, account_data):
        current_user = get_jwt_identity()

        try:
            account = AccountsService().create_account(
                account_data, current_user
            )
        except AlreadyExistsError:
            abort(409, message="Account already exists.")
        except DatabaseError:
            abort(500, message="Our engineering monkeys are having trouble")

        return account


@bp.route("/<uuid:account_id>")
class Account(MethodView):
    @jwt_required()
    @bp.response(200, AccountSchema)
    def get(self, account_id):
        current_user = get_jwt_identity()
        return AccountsService().get_account(account_id, current_user)

    @jwt_required()
    @bp.arguments(UpdateAccountSchema)
    @bp.response(200, AccountSchema)
    def put(self, account_data, account_id):
        current_user = get_jwt_identity()
        try:
            account = AccountsService().update_account(
                account_data, account_id, current_user
            )
        except AlreadyExistsError:
            abort(409, message="Account already exists.")
        return account

    @jwt_required(fresh=True)
    def delete(self, account_id):
        current_user = get_jwt_identity()

        try:
            AccountsService().delete_account(account_id, current_user)
        except ResourceInUseError:
            abort(
                400,
                message="The fault, dear user, is not in our server, but in ourselves, that we attempt to delete a referenced account.",
            )
        except DatabaseError:
            abort(
                500,
                message="Good news, everyone! Our servers are experiencing technical difficulties.",
            )

        return {"message": "Account deleted!"}
