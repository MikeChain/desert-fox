category_data = {"name": "test", "description": "test", "type": "income"}


def test_get_empty_categories(client, auth_tokens):
    response = client.get(
        "/v1/categories",
        headers={"Authorization": f"Bearer {auth_tokens['access_token']}"},
    )
    assert response.status_code == 200
    assert response.json == []


def test_std_user_create_category(client, auth_tokens):
    response = client.post(
        "/v1/categories",
        headers={"Authorization": f"Bearer {auth_tokens['access_token']}"},
        json=category_data,
    )
    assert response.status_code == 401


def test_create_category(client, admin_tokens):
    response = client.post(
        "/v1/categories",
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
        "/v1/categories",
        headers={"Authorization": f"Bearer {admin_tokens['access_token']}"},
        json={**category_data, "type": "invalid_type"},
    )
    assert response.status_code == 422


def test_create_existent_category(client, admin_tokens, category):
    response = client.post(
        "/v1/categories",
        headers={"Authorization": f"Bearer {admin_tokens['access_token']}"},
        json=category_data,
    )
    assert response.status_code == 409


def test_get_category(client, auth_tokens, category):
    response = client.get(
        "/v1/categories/1948b81b-42bf-4ea8-87f0-61a1416e3ffa",
        headers={"Authorization": f"Bearer {auth_tokens['access_token']}"},
    )
    assert response.status_code == 200
    json = response.json
    assert json["name"] == "test"
    assert json["description"] == "test"
    assert json["type"] == "income"


def test_get_unexistent_category(client, auth_tokens, category):
    response = client.get(
        "/v1/categories/1948b81b-42bf-4ea8-87f0-61a1416e3ff0",
        headers={"Authorization": f"Bearer {auth_tokens['access_token']}"},
    )
    assert response.status_code == 404
    print(response.json)
    assert (
        response.json["message"]
        == "This is not the category you are looking for."
    )


def test_user_update_category(client, auth_tokens, category):
    response = client.put(
        "/v1/categories/1948b81b-42bf-4ea8-87f0-61a1416e3ffa",
        headers={"Authorization": f"Bearer {auth_tokens['access_token']}"},
        json={"name": "new name", "description": "new description"},
    )
    assert response.status_code == 401


def test_admin_update_category(client, admin_tokens, category):
    response = client.put(
        "/v1/categories/1948b81b-42bf-4ea8-87f0-61a1416e3ffa",
        headers={"Authorization": f"Bearer {admin_tokens['access_token']}"},
        json={"name": "new name", "description": "new description"},
    )
    assert response.status_code == 201
    json = response.json
    assert json["name"] == "new name"
    assert json["description"] == "new description"
    assert json["type"] == "income"


def test_admin_delete_category(client, admin_tokens, category):
    response = client.delete(
        "/v1/categories/1948b81b-42bf-4ea8-87f0-61a1416e3ffa",
        headers={"Authorization": f"Bearer {admin_tokens['access_token']}"},
    )
    assert response.status_code == 200
    json = response.json
    assert json["message"] == "Category deleted!"


def test_no_admin_delete_category(client, transaction):
    response = client.delete(
        "/v1/categories/1948b81b-42bf-4ea8-87f0-61a1416e3ffa",
        headers={"Authorization": f"Bearer {transaction['access_token']}"},
    )
    assert response.status_code == 401
    json = response.json
    assert (
        json["message"]
        == "Nice try, slick. But you're not getting in without proper authorization."
    )


def test_no_admin_delete_category(client, admin_category_in_use):
    response = client.delete(
        "/v1/categories/1948b81b-42bf-4ea8-87f0-61a1416e3ffa",
        headers={
            "Authorization": f"Bearer {admin_category_in_use['access_token']}"
        },
    )
    assert response.status_code == 400
    json = response.json
    assert (
        json["message"]
        == "The fault, dear user, is not in our server, but in ourselves, that we attempt to delete a referenced category."
    )
