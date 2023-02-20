from flask.views import MethodView
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from flask_smorest import Blueprint, abort

from app.exceptions import DatabaseError, TotalMismatchError
from app.schemas import TransactionSchema
from app.services import TransactionsService

bp = Blueprint(
    "Transactions",
    __name__,
    description="Operations on transactions",
    url_prefix="/api/v1/transactions",
)


@bp.route("")
class Transactions(MethodView):
    @jwt_required()
    @bp.response(200, TransactionSchema(many=True))
    def get(self):
        user_id = get_jwt_identity()
        return TransactionsService().get_all_user_transactions(user_id)

    @jwt_required()
    @bp.arguments(TransactionSchema)
    @bp.response(201, TransactionSchema)
    def post(self, transaction_data):
        transaction_data["user_id"] = get_jwt_identity()
        try:
            transaction = TransactionsService().create_transaction(
                transaction_data
            )
        except TotalMismatchError:
            abort(400, message="Transaction amount and payment do not match.")
        except DatabaseError:
            abort(500, message="Our engineering monkeys are having trouble")

        return transaction
