import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.extensions import db


class PaymentAccountsModel(db.Model):
    __tablename__ = "payment_accounts"

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    account_id = db.Column(UUID(as_uuid=True), db.ForeignKey("accounts.id"))
    transaction_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("transactions.id")
    )
    subtotal_amount = db.Column(
        db.Numeric(precision=20, scale=4), nullable=False
    )

    db.Index("transaction_account_index", transaction_id),
    db.Index("account_index", account_id)
