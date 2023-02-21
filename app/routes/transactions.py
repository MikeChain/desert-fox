from flask import request
from flask.views import MethodView
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_smorest import Blueprint, abort

from app.exceptions import DatabaseError, TotalMismatchError
from app.schemas import (
    DetailsSchema,
    PaginatedTransactionSchema,
    PlainTransactionUpdateSchema,
    TransactionSchema,
)
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
    # @bp.response(200, TransactionSchema(many=True))
    def get(self):
        page = request.args.get("page", default=1, type=int)
        size = request.args.get("size", default=5, type=int)
        user_id = get_jwt_identity()
        schema = PaginatedTransactionSchema()
        t = TransactionsService().get_pagination(user_id, page, size)
        data = {"page": page, "per_page": size, "pages": t.pages}
        schema.load(data)
        return schema.dump(t)

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


@bp.route("/<uuid:transaction_id>")
class SingleTransaction(MethodView):
    @jwt_required()
    @bp.response(200, TransactionSchema)
    def get(self, transaction_id):
        user_id = get_jwt_identity()
        return TransactionsService().get_transaction(transaction_id, user_id)

    @jwt_required()
    @bp.arguments(PlainTransactionUpdateSchema)
    @bp.response(200, TransactionSchema)
    def put(self, transaction_data, transaction_id):
        user_id = get_jwt_identity()
        return TransactionsService().update_transaction(
            transaction_data, transaction_id, user_id
        )


@bp.route("/<uuid:transaction_id>/details")
class SingleTransactionDetails(MethodView):
    @jwt_required()
    @bp.response(200, DetailsSchema)
    def get(self, transaction_id):
        user_id = get_jwt_identity()
        return TransactionsService().get_transaction(transaction_id, user_id)

    @jwt_required()
    @bp.arguments(DetailsSchema)
    @bp.response(200, TransactionSchema)
    def put(self, details_data, transaction_id):
        user_id = get_jwt_identity()
        try:
            details = TransactionsService().update_details(
                details_data, transaction_id, user_id
            )
        except TotalMismatchError:
            abort(400, message="Transaction amount and payment do not match.")
        except DatabaseError:
            abort(
                500,
                message="Good news, everyone! Our servers are experiencing technical difficulties.",
            )

        return details
