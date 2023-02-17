import uuid

from sqlalchemy.exc import SQLAlchemyError

from app.exceptions import AlreadyExistsError, DatabaseError
from app.extensions import db
from app.models import AccountsModel


class AccountsService:
    def __init__(self):
        self.model = AccountsModel

    def get_all_user_accounts(self, user_id):
        return self.model.query.filter_by(user_id=user_id).all()

    def get_account(self, account_id, user_id):
        return self.model.query.filter_by(
            id=account_id, user_id=user_id
        ).first()

    def get_account_by_name(self, name, user_id):
        return self.model.query.filter_by(user_id=user_id, name=name).first()

    def create_account(self, account_data, user_id):
        account = self.get_account_by_name(account_data["name"], user_id)

        if account:
            raise AlreadyExistsError("Account already exists.")

        if not "initial_balance" in account_data:
            account_data["initial_balance"] = 0

        if "id" in account_data:
            account_data["id"] = uuid.UUID(account_data["id"]).hex

        account_data["user_id"] = user_id
        account = self.model(**account_data)

        try:
            db.session.add(account)
            db.session.commit()
        except SQLAlchemyError:
            raise DatabaseError

        return account

    def update_account(self, account_data, account_id, user_id):
        account = self.get_account(account_id, user_id)

        if "name" in account_data:
            acc = self.get_account_by_name(account_data["name"], user_id)

            if acc and account_id != acc.id:
                raise AlreadyExistsError("Account already exists.")
            account.name = account_data["name"]

        if "account_type" in account_data:
            account.account_type = account_data["account_type"]

        if "currency" in account_data:
            account.currency = account_data["currency"]

        if "initial_balance" in account_data:
            account.initial_balance = account_data["initial_balance"]

        try:
            db.session.add(account)
            db.session.commit()
        except SQLAlchemyError:
            raise DatabaseError

        return account
