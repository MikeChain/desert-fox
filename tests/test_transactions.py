import uuid


def test_get_empty_transactions(client, auth_tokens):
    response = client.get(
        "/v1/transactions",
        headers={"Authorization": f"Bearer {auth_tokens['access_token']}"},
    )
    assert response.status_code == 200
    assert response.json["items"] == []
    assert response.json["per_page"] == 5


def test_create_bad_transaction(client, auth_tokens):
    data = {
        "type": "expense",
        "transaction_date": "2023-01-01T00:00:00",
        "accounts": [{"account_id": uuid.uuid4(), "subtotal_amount": 15}],
        "transaction_details": [
            {
                "subcategory_id": uuid.uuid4(),
                "description": "test",
                "amount": 10,
            }
        ],
    }
    response = client.post(
        "/v1/transactions",
        headers={"Authorization": f"Bearer {auth_tokens['access_token']}"},
        json=data,
    )

    print(response.json)
    assert response.status_code == 400


def test_create_transaction_with_unexistent_keys(client, auth_tokens):
    data = {
        "type": "expense",
        "transaction_date": "2023-01-01T00:00:00",
        "accounts": [{"account_id": uuid.uuid4(), "subtotal_amount": 15}],
        "transaction_details": [
            {
                "subcategory_id": uuid.uuid4(),
                "description": "test",
                "amount": 10,
            },
            {
                "subcategory_id": uuid.uuid4(),
                "description": "test2",
                "amount": 5,
            },
        ],
    }
    response = client.post(
        "/v1/transactions",
        headers={"Authorization": f"Bearer {auth_tokens['access_token']}"},
        json=data,
    )

    print(response.json)
    assert response.status_code == 500


def test_create_good_transaction(client, transaction_data):
    data = {
        "type": "expense",
        "transaction_date": "2023-01-01T00:00:00",
        "accounts": [
            {
                "account_id": "c4fcca77-7731-4fec-9c7f-56c111e97075",
                "subtotal_amount": 15,
            }
        ],
        "transaction_details": [
            {
                "subcategory_id": "1bc759c6-60bf-4c25-bb80-7507e08e1ae2",
                "description": "test",
                "amount": 15,
            }
        ],
    }
    response = client.post(
        "/v1/transactions",
        headers={"Authorization": f"Bearer {transaction_data['access_token']}"},
        json=data,
    )

    print(response.json)
    assert response.status_code == 201


def test_get_inexistent_transaction(client, transaction):
    response = client.get(
        "/v1/transactions/d22af559-6084-45dd-b3ae-8019c1707043",
        headers={"Authorization": f"Bearer {transaction['access_token']}"},
    )

    assert response.status_code == 404


def test_get_transaction(client, transaction):
    response = client.get(
        "/v1/transactions/c22af559-6084-45dd-b3ae-8019c1707043",
        headers={"Authorization": f"Bearer {transaction['access_token']}"},
    )

    assert response.status_code == 200
    json = response.json
    assert json["id"] == "c22af559-6084-45dd-b3ae-8019c1707043"
    assert json["type"] == "expense"
    assert json["transaction_date"] == "2023-01-01T00:00:00"

    accounts = json["accounts"]
    details = json["transaction_details"]

    assert len(accounts) == 1
    assert len(details) == 1

    assert "id" not in accounts[0]
    assert accounts[0]["subtotal_amount"] == 15


def test_update_transaction(client, transaction):
    transaction_data = {"status": "verified", "notes": "test notes"}
    response = client.put(
        "/v1/transactions/c22af559-6084-45dd-b3ae-8019c1707043",
        headers={"Authorization": f"Bearer {transaction['access_token']}"},
        json=transaction_data,
    )

    assert response.status_code == 200
    json = response.json
    assert json["id"] == "c22af559-6084-45dd-b3ae-8019c1707043"
    assert json["type"] == "expense"
    assert json["status"] == "verified"
    assert json["notes"] == "test notes"

    response = client.put(
        "/v1/transactions/c22af559-6084-45dd-b3ae-8019c1707043",
        headers={"Authorization": f"Bearer {transaction['access_token']}"},
        json={"transaction_date": "2023-01-02T00:00:00"},
    )

    assert response.status_code == 405


def test_get_transaction_details(client, transaction):
    response = client.get(
        "/v1/transactions/c22af559-6084-45dd-b3ae-8019c1707043/details",
        headers={"Authorization": f"Bearer {transaction['access_token']}"},
    )

    assert response.status_code == 200
    json = response.json

    assert "accounts" in json
    assert "transaction_details" in json
    assert len(json) == 2


def test_update_transaction_details(client, transaction):
    update_data = {
        "transaction_details": [
            {
                "amount": 20.0,
                "description": "test",
                "id": "dd42f328-f0d6-4091-ae22-72ff088b18e4",
            }
        ],
        "accounts": [
            {
                "subtotal_amount": 20,
                "id": "ae93915c-bd48-4d40-bad9-1a3a03689a12",
            }
        ],
    }
    response = client.put(
        "/v1/transactions/c22af559-6084-45dd-b3ae-8019c1707043/details",
        headers={"Authorization": f"Bearer {transaction['access_token']}"},
        json=update_data,
    )

    assert response.status_code == 200
    json = response.json

    assert json["accounts"][0]["subtotal_amount"] == 20
    assert json["transaction_details"][0]["amount"] == 20
