import pytest
from app import create_app
from app.extensions import db, migrate

from config import envs


@pytest.fixture
def app():
    env = envs["qas"]
    app = create_app(environment=env)

    yield app


@pytest.fixture(scope="module")
def init_db(app):
    with app.app_context():
        migrate.upgrade()
        yield db
        migrate.downgrade(revision="base")


@pytest.fixture()
def client(app):
    return app.test_client()
