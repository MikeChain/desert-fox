import decimal
import uuid

from flask_smorest import abort
from sqlalchemy.exc import SQLAlchemyError

from app.exceptions import DatabaseError, TotalMismatchError
from app.extensions import db
from app.models import (
    PaymentAccountsModel,
    TransactionDetailsModel,
    TransactionsModel,
)
from app.services.subcategories import SubcategoriesService


class TransactionsService:
    def __init__(self):
        self.model = TransactionsModel
        self.details = TransactionDetailsModel
        self.accounts = PaymentAccountsModel
        self.tolerance = 0.01

    def get_all_user_transactions(self, user_id) -> list[TransactionsModel]:
        return self.model.query.filter_by(user_id=user_id).all()

    def get_pagination(self, user_id, page, size):
        return (
            self.model.query.filter_by(user_id=user_id)
            .order_by(self.model.transaction_date)
            .paginate(page=page, per_page=size)
        )

    def get_transaction(self, transaction_id, user_id) -> TransactionsModel:
        t = self.model.query.filter_by(
            id=transaction_id, user_id=user_id
        ).first()

        if t:
            return t
        abort(
            404,
            "Sorry, the transaction you are looking for is in another castle.",
        )

    def create_transaction(self, transaction_data) -> TransactionsModel:
        if "id" in transaction_data:
            transaction_data["id"] = uuid.UUID(transaction_data["id"]).hex
        else:
            transaction_data["id"] = uuid.uuid4()

        t_id = transaction_data["id"]
        t_type = transaction_data["type"]

        details = self._create_details(
            self.details,
            transaction_data["transaction_details"],
            t_id,
        )

        accounts = self._create_details(
            self.accounts,
            transaction_data["accounts"],
            t_id,
        )

        for account in accounts:
            account.type = t_type

        total_a = self._get_totals(details, accounts)

        del transaction_data["transaction_details"]
        del transaction_data["accounts"]

        transaction_data["total_amount"] = total_a
        transaction_data["status"] = "pending"

        transaction = self.model(**transaction_data)

        try:
            db.session.add(transaction)
            db.session.add_all(details)
            db.session.add_all(accounts)
            db.session.commit()
        except SQLAlchemyError:
            raise DatabaseError

        return transaction

    def update_transaction(
        self, transaction_data, transaction_id, user_id
    ) -> TransactionsModel:
        transaction = self._get_transaction_for_update(transaction_id, user_id)

        if "status" in transaction_data:
            transaction.status = transaction_data["status"]

        if "transaction_date" in transaction_data:
            transaction.transaction_date = transaction_data["transaction_date"]

        if "notes" in transaction_data:
            transaction.notes = transaction_data["notes"]

        try:
            db.session.add(transaction)
            db.session.commit()
        except SQLAlchemyError:
            raise DatabaseError

        return transaction

    def update_details(
        self, details_data, transaction_id, user_id
    ) -> TransactionsModel:
        transaction = self._get_transaction_for_update(transaction_id, user_id)

        accounts = self._get_accounts(transaction_id)
        details = self._get_details(transaction_id)

        if "accounts" in details_data:
            for account in details_data["accounts"]:
                accounts[account["id"]].subtotal_amount = account[
                    "subtotal_amount"
                ]

        if "transaction_details" in details_data:
            for detail in details_data["transaction_details"]:
                if "subcategory_id" in detail:
                    sbc = detail["subcategory_id"]
                    if SubcategoriesService().get_subcategory(sbc, user_id):
                        details[detail["id"]].subcategory_id = sbc

                if "description" in detail:
                    details[detail["id"]].description = detail["description"]

                if "amount" in detail:
                    details[detail["id"]].amount = detail["amount"]

        total = self._get_totals(
            list(details.values()), list(accounts.values())
        )

        try:
            if abs(transaction.total_amount - total) > self.tolerance:
                transaction.total_amount = total

                db.session.add(transaction)

            db.session.add_all(
                [
                    accounts[account["id"]]
                    for account in details_data["accounts"]
                ]
            )
            db.session.add_all(
                [
                    details[detail["id"]]
                    for detail in details_data["transaction_details"]
                ]
            )
            db.session.commit()
        except SQLAlchemyError:
            raise DatabaseError

        return transaction

    @staticmethod
    def _create_details(
        model, data, id
    ) -> list[PaymentAccountsModel | TransactionDetailsModel]:
        return [model(**x, transaction_id=id) for x in data]

    def _get_totals(self, details: list, accounts: list) -> decimal.Decimal:
        total_d = sum(d.amount for d in details)
        total_a = sum(a.subtotal_amount for a in accounts)

        if abs(total_a - total_d) > self.tolerance:
            raise TotalMismatchError

        return decimal.Decimal(total_a)

    def _get_transaction_for_update(
        self, transaction_id, user_id
    ) -> TransactionsModel:
        transaction = self.get_transaction(transaction_id, user_id)

        if transaction.status != "pending":
            abort(
                405,
                message="This transaction has already made an offer it couldn't refuse.",
            )

        return transaction

    def _get_accounts(self, transaction_id):
        accounts = self.accounts.query.filter_by(
            transaction_id=transaction_id
        ).all()

        return {a.id: a for a in accounts}

    def _get_details(self, transaction_id):
        details = self.details.query.filter_by(
            transaction_id=transaction_id
        ).all()

        return {d.id: d for d in details}
