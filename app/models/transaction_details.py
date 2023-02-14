import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.extensions import db


class TransactionDetailsModel(db.Model):
    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    transaction_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("transactions.id")
    )
    subcategory_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("subcategories.id")
    )
    description = db.Column(db.String(255), nullable=False)
    amount = db.Column(db.Numeric(precision=20, scale=4), nullable=False)

    created_at = db.Column(
        db.DateTime, nullable=False, server_default=func.now()
    )

    transaction = db.relationship(
        "TransactionsModel", back_populates="transaction_details"
    )
    subcategory = db.relationship(
        "SubcategoriesModel", back_populates="transaction_details"
    )

    db.Index("transaction_details_index", transaction_id),
    db.Index("subcategory_details_index", subcategory_id)
