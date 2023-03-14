def test_get_non_admin(client, auth_tokens):
    response = client.get(
        "/v1/users",
        headers={"Authorization": f"Bearer {auth_tokens['access_token']}"},
    )
    assert response.status_code == 401


def test_get_admin(client, admin_tokens):
    response = client.get(
        "/v1/users",
        headers={"Authorization": f"Bearer {admin_tokens['access_token']}"},
    )
    print(admin_tokens["access_token"])
    assert response.status_code == 200
    assert len(response.json) == 1


def test_update_user(client, auth_tokens):
    response = client.put(
        "/v1/users/6e4987c5-851f-4eda-89bc-fb8b8fbd518a",
        headers={"Authorization": f"Bearer {auth_tokens['access_token']}"},
        json={"display_name": "test name"},
    )
    assert response.status_code == 200
    assert response.json["display_name"] == "test name"


def test_get_user(client, auth_tokens):
    response = client.get(
        "/v1/users/6e4987c5-851f-4eda-89bc-fb8b8fbd518a",
        headers={"Authorization": f"Bearer {auth_tokens['access_token']}"},
    )
    assert response.status_code == 200
    assert response.json["email"] == "testuser@example.com"
