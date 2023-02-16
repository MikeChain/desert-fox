from sqlalchemy.exc import SQLAlchemyError

from app.exceptions import DatabaseError
from app.extensions import db
from app.models import TransactionsModel


class TransactionsService:
    def __init__(self):
        self.model = TransactionsModel

    def get_all_user_transactions(self, user_id):
        return self.model.query.filter_by(user_id=user_id).all()

    def create_transaction(self, transaction_data):
        transaction = self.model(**transaction_data)

        try:
            db.session.add(transaction)

            db.session.commit()
        except SQLAlchemyError:
            raise DatabaseError

        return transaction
