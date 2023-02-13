import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.extensions import db


class CategoriesModel(db.Model):
    __tablename__ = "categories"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    name = db.Column(db.String(25), nullable=False)
    description = db.Column(db.String(100))
    type = db.Column(db.Enum("income", "expense", name="transaction_type"))
    created_at = db.Column(
        db.DateTime, nullable=False, server_default=func.now()
    )

    subcategories = db.relationship(
        "SubcategoriesModel",
        lazy="dynamic",
        back_populates="category",
        cascade="all, delete",
    )
