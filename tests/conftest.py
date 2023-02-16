import uuid

import pytest

import app.models
from app import create_app
from app.extensions import db
from app.services import UserService
from config import envs

user_data = {
    "email": "testuser@example.com",
    "password": "testpassword",
    "id": uuid.UUID("6e4987c5-851f-4eda-89bc-fb8b8fbd518a").hex,
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
