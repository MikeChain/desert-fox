import pytest

from app.services import CategoriesService

category_data = {"name": "test", "description": "test", "type": "income"}


@pytest.fixture()
def category():
    CategoriesService().create_category(category_data)


def test_get_empty_categories(client, auth_tokens):
    response = client.get(
        "/api/v1/categories",
        headers={"Authorization": f"Bearer {auth_tokens['access_token']}"},
    )
    assert response.status_code == 200
    assert response.json == []


def test_std_user_create_category(client, auth_tokens):
    response = client.post(
        "/api/v1/categories",
        headers={"Authorization": f"Bearer {auth_tokens['access_token']}"},
        json=category_data,
    )
    assert response.status_code == 401


def test_create_category(client, admin_tokens):
    response = client.post(
        "/api/v1/categories",
        headers={"Authorization": f"Bearer {admin_tokens['access_token']}"},
        json=category_data,
    )
    assert response.status_code == 201

    json = response.json
    assert json["name"] == "test"
    assert json["description"] == "test"
    assert json["type"] == "income"


def test_create_bad_category(client, admin_tokens):
    response = client.post(
        "/api/v1/categories",
        headers={"Authorization": f"Bearer {admin_tokens['access_token']}"},
        json={**category_data, "type": "invalid_type"},
    )
    assert response.status_code == 422


def test_create_existent_category(client, admin_tokens, category):
    response = client.post(
        "/api/v1/categories",
        headers={"Authorization": f"Bearer {admin_tokens['access_token']}"},
        json=category_data,
    )
    assert response.status_code == 409
