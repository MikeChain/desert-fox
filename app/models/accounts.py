import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.extensions import db


class AccountsModel(db.Model):
    __tablename__ = "accounts"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False
    )
    name = db.Column(db.String(25), nullable=False)
    account_type = db.Column(
        db.Enum("cash", "debit", "credit", name="account_type"), nullable=False
    )
    currency = db.Column(
        db.Enum("MXN", "USD", "EUR", name="currency_id"),
        nullable=False,
        server_default="MXN",
    )
    created_at = db.Column(
        db.DateTime, nullable=False, server_default=func.now()
    )
    initial_balance = db.Column(
        db.Numeric(precision=20, scale=4), nullable=False, default=0
    )

    db.Index("accounts_user_id_index", user_id)
    user = db.relationship("UserModel", back_populates="accounts")
    transactions = db.relationship(
        "TransactionsModel",
        secondary="payment_accounts",
        back_populates="accounts",
        lazy="dynamic",
    )
