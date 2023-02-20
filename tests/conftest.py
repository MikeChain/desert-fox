import uuid

import pytest
from flask_jwt_extended import decode_token

import app.models
from app import create_app
from app.extensions import db
from app.services import (
    AccountsService,
    CategoriesService,
    SubcategoriesService,
    TransactionsService,
    UserService,
)
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
def admin():
    UserService().create_user(
        {
            "email": "test_user@example.com",
            "password": "testpassword",
            "user_type": "admin",
            "id": uuid.UUID("6e4987c5-851f-4eda-89bc-fb8b8fbd518a").hex,
        }
    )


@pytest.fixture()
def admin_tokens(admin):
    tokens = UserService().authenticate(
        "test_user@example.com", user_data["password"]
    )
    return tokens


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


@pytest.fixture()
def category():
    CategoriesService().create_category(
        {
            "name": "test",
            "description": "test",
            "type": "income",
            "id": "1948b81b-42bf-4ea8-87f0-61a1416e3ffa",
        }
    )


@pytest.fixture()
def default_subcategory(category):
    UserService().create_user(
        {
            "email": "test_user@example.com",
            "password": "testpassword",
            "user_type": "admin",
            "id": uuid.UUID("7e4987c5-851f-4eda-89bc-fb8b8fbd518a").hex,
        }
    )
    SubcategoriesService().create_subcategory(
        {
            "id": "1bc759c6-60bf-4c25-bb80-7507e08e1ae2",
            "name": "test",
            "category_id": "1948b81b-42bf-4ea8-87f0-61a1416e3ffa",
            "user_id": "7e4987c5-851f-4eda-89bc-fb8b8fbd518a",
            "is_default": True,
        }
    )


@pytest.fixture()
def subcategory(category):
    UserService().create_user(
        {
            "email": "test_user@example.com",
            "password": "testpassword",
            "user_type": "admin",
            "id": uuid.UUID("7e4987c5-851f-4eda-89bc-fb8b8fbd518a").hex,
        }
    )
    SubcategoriesService().create_subcategory(
        {
            "id": "1bc759c6-60bf-4c25-bb80-7507e08e1ae2",
            "name": "test",
            "category_id": "1948b81b-42bf-4ea8-87f0-61a1416e3ffa",
            "user_id": "7e4987c5-851f-4eda-89bc-fb8b8fbd518a",
            "is_default": False,
        }
    )


@pytest.fixture()
def transaction_data(category):
    current_user_id = "7e4987c5-851f-4eda-89bc-fb8b8fbd518a"
    user_email = "test_user@example.com"
    user_password = "testpassword"
    UserService().create_user(
        {
            "email": user_email,
            "password": user_password,
            "user_type": "pro",
            "id": uuid.UUID(current_user_id).hex,
        }
    )
    SubcategoriesService().create_subcategory(
        {
            "id": "1bc759c6-60bf-4c25-bb80-7507e08e1ae2",
            "name": "test",
            "category_id": "1948b81b-42bf-4ea8-87f0-61a1416e3ffa",
            "user_id": current_user_id,
            "is_default": False,
        }
    )
    AccountsService().create_account(account_data, current_user_id)
    return UserService().authenticate(user_email, user_password)


@pytest.fixture()
def transaction(category):
    current_user_id = "7e4987c5-851f-4eda-89bc-fb8b8fbd518a"
    user_email = "test_user@example.com"
    user_password = "testpassword"
    UserService().create_user(
        {
            "email": user_email,
            "password": user_password,
            "user_type": "pro",
            "id": uuid.UUID(current_user_id).hex,
        }
    )
    SubcategoriesService().create_subcategory(
        {
            "id": "1bc759c6-60bf-4c25-bb80-7507e08e1ae2",
            "name": "test",
            "category_id": "1948b81b-42bf-4ea8-87f0-61a1416e3ffa",
            "user_id": current_user_id,
            "is_default": False,
        }
    )
    AccountsService().create_account(account_data, current_user_id)
    TransactionsService().create_transaction(
        {
            "id": "c22af559-6084-45dd-b3ae-8019c1707043",
            "user_id": current_user_id,
            "type": "expense",
            "transaction_date": "2023-01-01T00:00:00",
            "accounts": [
                {
                    "account_id": "c4fcca77-7731-4fec-9c7f-56c111e97075",
                    "subtotal_amount": 15,
                    "id": "ae93915c-bd48-4d40-bad9-1a3a03689a12",
                }
            ],
            "transaction_details": [
                {
                    "subcategory_id": "1bc759c6-60bf-4c25-bb80-7507e08e1ae2",
                    "description": "test",
                    "amount": 15,
                    "id": "dd42f328-f0d6-4091-ae22-72ff088b18e4",
                }
            ],
        }
    )
    return UserService().authenticate(user_email, user_password)


@pytest.fixture()
def admin_category_in_use(category):
    current_user_id = "7e4987c5-851f-4eda-89bc-fb8b8fbd518a"
    user_email = "test_user@example.com"
    user_password = "testpassword"
    UserService().create_user(
        {
            "email": user_email,
            "password": user_password,
            "user_type": "admin",
            "id": uuid.UUID(current_user_id).hex,
        }
    )
    SubcategoriesService().create_subcategory(
        {
            "id": "1bc759c6-60bf-4c25-bb80-7507e08e1ae2",
            "name": "test",
            "category_id": "1948b81b-42bf-4ea8-87f0-61a1416e3ffa",
            "user_id": current_user_id,
            "is_default": False,
        }
    )
    return UserService().authenticate(user_email, user_password)
