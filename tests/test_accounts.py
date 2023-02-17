account_data = {
    "name": "test_account",
    "account_type": "cash",
    "currency": "MXN",
    "initial_balance": 0,
}


def test_get_user_empty_accounts(client, auth_tokens):
    response = client.get(
        "/api/v1/accounts",
        headers={"Authorization": f"Bearer {auth_tokens['access_token']}"},
    )
    assert response.status_code == 200
    assert response.json == []


def test_get_user_accounts(client, auth_tokens, account):
    response = client.get(
        "/api/v1/accounts",
        headers={"Authorization": f"Bearer {auth_tokens['access_token']}"},
    )
    assert response.status_code == 200
    assert len(response.json) == 1

    ac = response.json[0]

    assert ac["name"] == "test_account"
    assert ac["account_type"] == "cash"
    assert ac["currency"] == "MXN"


def test_create_new_account(client, auth_tokens):
    response = client.post(
        "/api/v1/accounts",
        headers={"Authorization": f"Bearer {auth_tokens['access_token']}"},
        json=account_data,
    )

    assert response.status_code == 201


def test_create_existent_account(client, auth_tokens, account):
    response = client.post(
        "/api/v1/accounts",
        headers={"Authorization": f"Bearer {auth_tokens['access_token']}"},
        json=account_data,
    )

    assert response.status_code == 409


def test_create_bad_account(client, auth_tokens, account):
    ad = {"name": "test_account", "account_type": "cash"}
    response = client.post(
        "/api/v1/accounts",
        headers={"Authorization": f"Bearer {auth_tokens['access_token']}"},
        json=ad,
    )

    assert response.status_code == 422


def test_get_account(client, auth_tokens, account):
    response = client.get(
        "/api/v1/accounts/c4fcca77-7731-4fec-9c7f-56c111e97075",
        headers={"Authorization": f"Bearer {auth_tokens['access_token']}"},
    )
    assert response.status_code == 200

    assert response.json["name"] == "test_account"
    assert response.json["account_type"] == "cash"
    assert response.json["currency"] == "MXN"


def test_update_account(client, auth_tokens, account):
    response = client.put(
        "/api/v1/accounts/c4fcca77-7731-4fec-9c7f-56c111e97075",
        headers={"Authorization": f"Bearer {auth_tokens['access_token']}"},
        json={"name": "test account updated"},
    )
    assert response.status_code == 200

    assert response.json["name"] == "test account updated"
    assert response.json["account_type"] == "cash"
    assert response.json["currency"] == "MXN"
