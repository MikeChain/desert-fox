import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.extensions import db


class SubcategoriesModel(db.Model):
    __tablename__ = "subcategories"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    name = db.Column(db.String(25), nullable=False)
    user_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("users.id"), nullable=False
    )
    category_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("categories.id"), nullable=False
    )
    created_at = db.Column(
        db.DateTime, nullable=False, server_default=func.now()
    )
    is_default = db.Column(db.Boolean)
    is_active = db.Column(db.Boolean)

    db.Index("subcategories_user_id_index", "user_id")
    user = db.relationship("UserModel", back_populates="subcategories")
    category = db.relationship(
        "CategoriesModel", back_populates="subcategories"
    )
    transaction_details = db.relationship(
        "TransactionDetailsModel",
        lazy="dynamic",
        back_populates="subcategory",
        cascade="all, delete",
    )
