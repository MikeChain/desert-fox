import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.extensions import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    display_name = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, server_default=func.now())
    last_password_change = db.Column(db.Date)
    last_login = db.Column(db.Date)
    user_type = db.Column(db.Enum("admin", "pro", "standard", name="user_type"))
    preferred_language_code = db.Column(
        db.Enum("es", "en", name="preferred_language_code")
    )
