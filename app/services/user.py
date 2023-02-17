import uuid
from datetime import date

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    decode_token,
)
from passlib.hash import pbkdf2_sha512
from sqlalchemy.exc import SQLAlchemyError

from app.exceptions import (
    AlreadyExistsError,
    AuthenticationFailedException,
    DatabaseError,
    UserNotFoundException,
)
from app.extensions import db
from app.models import UserModel


class UserService:
    def __init__(self):
        self.model = UserModel

    def get_all_users(self):
        return self.model.query.all()

    def get_user(self, user_id):
        return self.model.query.get(user_id)

    def get_user_404(self, user_id):
        return self.model.query.get_or_404(user_id)

    def get_user_by_email(self, email):
        return self.model.query.filter_by(email=email).first()

    def create_user(self, user_data):
        user = self.get_user_by_email(user_data["email"])

        if user:
            raise AlreadyExistsError("Email already exists.")

        data = {
            **user_data,
            "password": self._hash_password(user_data["password"]),
            "preferred_language_code": user_data.get(
                "preferred_language_code", "es"
            ),
        }

        if "id" in user_data:
            data["id"] = uuid.UUID(user_data["id"]).hex

        user = self.model(**data)

        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            raise DatabaseError

        return user

    def authenticate(self, email, password):
        user = self.get_user_by_email(email)

        if user is None:
            raise UserNotFoundException

        if not pbkdf2_sha512.verify(password, user.password):
            raise AuthenticationFailedException

        if user.last_login != date.today():
            user.last_login = date.today()
            db.session.add(user)
            db.session.commit()

        additional_claims = {
            "u_type": user.user_type,
            "lang": user.preferred_language_code,
        }
        refresh_token = create_refresh_token(
            identity=user.id, additional_claims=additional_claims
        )

        additional_claims["r_jti"] = decode_token(refresh_token)["jti"]

        access_token = create_access_token(
            identity=user.id,
            fresh=True,
            additional_claims=additional_claims,
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

    def update(self, user_data, user_id):
        user = self.get_user_404(user_id)

        if "name" in user_data:
            u = self.get_user_by_email(user_data["email"])

            if u and user_id != u.id:
                raise AlreadyExistsError("Email already exists.")
            user.email = user_data.get("email", user.email)

        if "password" in user_data:
            user.password = self._hash_password(user_data["password"])

        user.display_name = user_data.get("display_name", user.display_name)

        user.preferred_language_code = user_data.get(
            "preferred_language_code", user.preferred_language_code
        )

        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            raise DatabaseError

        return user

    @staticmethod
    def _hash_password(password):
        return pbkdf2_sha512.hash(password)
