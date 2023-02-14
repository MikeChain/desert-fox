import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.extensions import db


class TransactionsModel(db.Model):
    __tablename__ = "transactions"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    user_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False
    )
    type = db.Column(
        db.Enum("income", "expense", name="transaction_type"), nullable=False
    )
    status = db.Column(
        db.Enum("pending", "verified", "rejected", name="transaction_status"),
        nullable=False,
    )
    total_amount = db.Column(db.DECIMAL, nullable=False, default=0)
    transaction_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(
        db.DateTime, nullable=False, server_default=func.now()
    )
    notes = db.Column(db.String(255))

    db.Index("transactions_user_id_index", user_id)
    user = db.relationship("UserModel", back_populates="transactions")
