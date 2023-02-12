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
    data = {"email": "testuser@example.com", "password": "testpassword"}
    UserService().create_user(data)
