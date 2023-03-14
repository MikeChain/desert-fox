import json

from flask_jwt_extended import decode_token
from passlib.hash import pbkdf2_sha512

from app.models import UserModel


def test_register(client):
    # Preparar los datos de prueba
    test_email = "testuser@example.com"
    test_pass = "testpassword"
    test_name = "Test User"

    data = {
        "email": test_email,
        "password": test_pass,
        "display_name": test_name,
    }

    # Enviar una solicitud de POST al endpoint de registro
    response = client.post("/v1/auth/register", json=data)

    # Verificar que la respuesta sea exitosa (status code 201)
    assert response.status_code == 201

    user = UserModel.query.filter_by(email=test_email).first()

    assert user is not None
    assert user.email == test_email
    assert user.display_name == test_name
    assert not user.password == test_pass
    assert pbkdf2_sha512.verify(test_pass, user.password)
    assert user.user_type == "standard"

    j_data = json.loads(response.get_data(as_text=True))
    assert "id" in j_data
    assert "email" in j_data
    assert "display_name" in j_data
    assert "preferred_language_code" in j_data
    assert "password" not in j_data

    assert j_data["preferred_language_code"] == "es"


def test_register_existent_user(client, user):
    data = {"email": "testuser@example.com", "password": "testpassword"}
    response = client.post("/v1/auth/register", json=data)
    assert response.status_code == 409
    j_data = json.loads(response.get_data(as_text=True))
    assert j_data["message"] == "Email already exists."


def test_login(client, user):
    data = {"email": "testuser@example.com", "password": "testpassword"}

    response = client.post("/v1/auth/login", json=data)

    token = decode_token(response.json["access_token"])

    assert token["sub"] == "6e4987c5-851f-4eda-89bc-fb8b8fbd518a"

    assert response.status_code == 200
    assert "access_token" in response.json
    assert "refresh_token" in response.json


def test_login_failed(client, user):
    data = {"email": "testuser@example.com", "password": "other_password"}

    response = client.post("/v1/auth/login", json=data)

    assert response.status_code == 401
    assert "You shall not pass." == response.json["message"]
    assert "Unauthorized" == response.json["status"]


def test_login_unexistent(client):
    data = {"email": "testuser@example.com", "password": "testpassword"}

    response = client.post("/v1/auth/login", json=data)
    assert response.status_code == 404


def test_logout(client, auth_tokens):
    response = client.post("/v1/auth/logout")

    # intentar hacer logout sin token
    assert response.status_code == 401

    response = client.post(
        "/v1/auth/logout",
        headers={"Authorization": f"Bearer {auth_tokens['access_token']}"},
    )
    assert response.status_code == 200

    # token inválido
    response = client.post(
        "/v1/auth/logout",
        headers={"Authorization": f"Bearer {auth_tokens['access_token']}"},
    )
    assert response.status_code == 401


def test_refresh(client, auth_tokens):
    token = auth_tokens["refresh_token"]

    response = client.post(
        "/v1/auth/refresh",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json

    tk = decode_token(response.json["access_token"])

    print(tk)

    assert tk["fresh"] == False
    assert tk["type"] == "access"


def test_refresh_with_access_token(client, auth_tokens):
    token = auth_tokens["access_token"]

    response = client.post(
        "/v1/auth/refresh",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 401
    assert response.json["message"] == "Signature verification failed."
    assert response.json["error"] == "invalid_token"


def test_expired_token(client, short_tokens):
    import time

    time.sleep(1)
    response = client.post("/v1/auth/logout")
    response = client.post(
        "/v1/auth/logout",
        headers={"Authorization": f"Bearer {short_tokens['access_token']}"},
    )
    assert response.status_code == 401
    assert response.json["message"] == "The token has expired"
    assert response.json["error"] == "token_expired"
