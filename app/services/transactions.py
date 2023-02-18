import uuid

from sqlalchemy.exc import SQLAlchemyError

from app.exceptions import DatabaseError, TotalMismatchError
from app.extensions import db
from app.models import (
    PaymentAccountsModel,
    TransactionDetailsModel,
    TransactionsModel,
)


class TransactionsService:
    def __init__(self):
        self.model = TransactionsModel
        self.details = TransactionDetailsModel
        self.accounts = PaymentAccountsModel
        self.tolerance = 0.01

    def get_all_user_transactions(self, user_id):
        return self.model.query.filter_by(user_id=user_id).all()

    def create_transaction(self, transaction_data):
        if "id" in transaction_data:
            transaction_data["id"] = uuid.UUID(transaction_data["id"]).hex
        else:
            transaction_data["id"] = uuid.uuid4()

        details = self._get_details(
            self.details,
            transaction_data["transaction_details"],
            transaction_data["id"],
        )

        accounts = self._get_details(
            self.accounts,
            transaction_data["payment_accounts"],
            transaction_data["id"],
        )

        total_d = sum(d.amount for d in details)
        total_a = sum(a.subtotal_amount for a in accounts)

        if abs(total_a - total_d) > self.tolerance:
            raise TotalMismatchError

        del transaction_data["transaction_details"]
        del transaction_data["payment_accounts"]

        transaction_data["total_amount"] = total_a
        transaction_data["status"] = "pending"

        transaction = self.model(**transaction_data)

        try:
            db.session.add(transaction)

            for d in details:
                db.session.add(d)

            for a in accounts:
                db.session.add(a)

            db.session.commit()
        except SQLAlchemyError:
            raise DatabaseError

        return transaction

    @staticmethod
    def _get_details(model, data, id):
        return [model(**x, transaction_id=id) for x in data]
