import uuid

import pytest
from flask_jwt_extended import decode_token

import app.models
from app import create_app
from app.extensions import db
from app.services import AccountsService, UserService
from config import envs

user_data = {
    "email": "testuser@example.com",
    "password": "testpassword",
    "id": uuid.UUID("6e4987c5-851f-4eda-89bc-fb8b8fbd518a").hex,
}

account_data = {
    "id": uuid.UUID("c4fcca77-7731-4fec-9c7f-56c111e97075").hex,
    "name": "test_account",
    "account_type": "cash",
    "currency": "MXN",
    "initial_balance": 0,
}


@pytest.fixture
def app():
    env = envs["qas"]
    app = create_app(environment=env)

    with app.app_context():
        db.create_all()
        yield app
        db.session.close()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def user():
    UserService().create_user(user_data)


@pytest.fixture()
def auth_tokens(user):
    tokens = UserService().authenticate(
        user_data["email"], user_data["password"]
    )
    return tokens


@pytest.fixture()
def short_tokens(app):
    UserService().create_user(user_data)
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 1
    tokens = UserService().authenticate(
        user_data["email"], user_data["password"]
    )
    return tokens


@pytest.fixture()
def account(auth_tokens):
    tk = decode_token(auth_tokens["access_token"])

    current_user = tk["sub"]
    AccountsService().create_account(account_data, current_user)
