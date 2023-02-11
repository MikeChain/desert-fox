def test_index_route(client):
    response = client.get("/test")
    assert (
        "<h1>Probando el patrón de fábrica de aplicaciones Flask</h1>".encode(
            "utf-8"
        )
        in response.data
    )
