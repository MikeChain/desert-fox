import uuid


def test_get_empty_transactions(client, auth_tokens):
    response = client.get(
        "/api/v1/transactions",
        headers={"Authorization": f"Bearer {auth_tokens['access_token']}"},
    )
    assert response.status_code == 200
    assert response.json == []


def test_create_bad_transaction(client, auth_tokens):
    data = {
        "type": "expense",
        "transaction_date": "2023-01-01T00:00:00",
        "payment_accounts": [
            {"account_id": uuid.uuid4(), "subtotal_amount": 15}
        ],
        "transaction_details": [
            {
                "subcategory_id": uuid.uuid4(),
                "description": "test",
                "amount": 10,
            }
        ],
    }
    response = client.post(
        "/api/v1/transactions",
        headers={"Authorization": f"Bearer {auth_tokens['access_token']}"},
        json=data,
    )

    print(response.json)
    assert response.status_code == 400


def test_create_transaction_with_unexistent_keys(client, auth_tokens):
    data = {
        "type": "expense",
        "transaction_date": "2023-01-01T00:00:00",
        "payment_accounts": [
            {"account_id": uuid.uuid4(), "subtotal_amount": 15}
        ],
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
        "/api/v1/transactions",
        headers={"Authorization": f"Bearer {auth_tokens['access_token']}"},
        json=data,
    )

    print(response.json)
    assert response.status_code == 500
