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
