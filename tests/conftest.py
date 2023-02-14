import uuid

import pytest

import app.models
from app import create_app
from app.extensions import db
from app.services import UserService
from config import envs


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
    data = {
        "email": "testuser@example.com",
        "password": "testpassword",
        "id": uuid.UUID("6e4987c5-851f-4eda-89bc-fb8b8fbd518a").hex,
    }
    UserService().create_user(data)
