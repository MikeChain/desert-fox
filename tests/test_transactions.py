def test_get_empty_transactions(client, auth_tokens):
    response = client.get(
        "/api/v1/transactions",
        headers={"Authorization": f"Bearer {auth_tokens['access_token']}"},
    )
    assert response.status_code == 200
    assert response.json == []
