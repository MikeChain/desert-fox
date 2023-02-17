from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_smorest import Blueprint, abort

from app.exceptions import AlreadyExistsError, DatabaseError
from app.schemas import AccountSchema, UpdateAccountSchema
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
    @bp.response(200, AccountSchema(many=True))
    def get(self):
        current_user = get_jwt_identity()
        return AccountsService().get_all_user_accounts(current_user)

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
