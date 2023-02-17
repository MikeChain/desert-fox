subcategory_data = {
    "name": "test",
    "category_id": "1948b81b-42bf-4ea8-87f0-61a1416e3ffa",
}


def test_get_empty_subcategories(client, auth_tokens):
    response = client.get(
        "/api/v1/subcategories",
        headers={"Authorization": f"Bearer {auth_tokens['access_token']}"},
    )
    assert response.status_code == 200
    assert response.json == []


def test_std_user_create_subcategory(client, auth_tokens):
    response = client.post(
        "/api/v1/subcategories",
        headers={"Authorization": f"Bearer {auth_tokens['access_token']}"},
        json=subcategory_data,
    )
    assert response.status_code == 401


def test_admin_create_subcategory_without_category(client, admin_tokens):
    response = client.post(
        "/api/v1/subcategories",
        headers={"Authorization": f"Bearer {admin_tokens['access_token']}"},
        json=subcategory_data,
    )
    assert response.status_code == 500


def test_admin_create_subcategory(client, admin_tokens, category):
    response = client.post(
        "/api/v1/subcategories",
        headers={"Authorization": f"Bearer {admin_tokens['access_token']}"},
        json=subcategory_data,
    )
    assert response.status_code == 201


def test_get_default_subcategory(client, auth_tokens, default_subcategory):
    response = client.get(
        "/api/v1/subcategories/1bc759c6-60bf-4c25-bb80-7507e08e1ae2",
        headers={"Authorization": f"Bearer {auth_tokens['access_token']}"},
    )
    assert response.status_code == 200


def test_get_non_default_subcategory(client, auth_tokens, subcategory):
    response = client.get(
        "/api/v1/subcategories/1bc759c6-60bf-4c25-bb80-7507e08e1ae2",
        headers={"Authorization": f"Bearer {auth_tokens['access_token']}"},
    )
    assert response.status_code == 404
