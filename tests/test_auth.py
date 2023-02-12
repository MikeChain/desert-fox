import json

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
    response = client.post("/auth/register", json=data)

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


def test_register_existent_user(client):
    data = {"email": "testuser@example.com", "password": "testpassword"}

    # Enviar una solicitud de POST al endpoint de registro
    response = client.post("/auth/register", json=data)
    assert response.status_code == 201

    response = client.post("/auth/register", json=data)
    assert response.status_code == 409
    j_data = json.loads(response.get_data(as_text=True))
    assert j_data["message"] == "Email already exists."


def test_login(client):
    data = {"email": "testuser@example.com", "password": "testpassword"}

    # Enviar una solicitud de POST al endpoint de registro
    response = client.post("/auth/register", json=data)
    assert response.status_code == 201

    # Enviar una solicitud de POST al endpoint de inicio de sesión
    response = client.post("/auth/login", json=data)

    assert response.status_code == 200
    assert "access_token" in response.json
    assert "refresh_token" in response.json


def test_login_failed(client):
    data = {"email": "testuser@example.com", "password": "testpassword"}

    # Enviar una solicitud de POST al endpoint de registro
    response = client.post("/auth/register", json=data)
    assert response.status_code == 201

    data["password"] = "other_password"
    response = client.post("/auth/login", json=data)

    assert response.status_code == 401
    assert "You shall not pass." == response.json["message"]
    assert "Unauthorized" == response.json["status"]


def test_login_non_existent(client):
    data = {"email": "testuser@example.com", "password": "testpassword"}

    response = client.post("/auth/login", json=data)
    assert response.status_code == 404
