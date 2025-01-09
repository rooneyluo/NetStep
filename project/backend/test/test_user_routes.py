import pytest
from fastapi.testclient import TestClient
from main import app
from model.user_model import UserResponse, UserLogin
from unittest.mock import patch

client = TestClient(app)

@pytest.fixture
def mock_add_user():
    with patch("routes.user_routes.add_user") as mock:
        yield mock

@pytest.fixture
def mock_get_user_for_authentication():
    with patch("routes.user_routes.get_user_for_authentication") as mock:
        yield mock

@pytest.fixture
def mock_verify_password():
    with patch("routes.user_routes.verify_password") as mock:
        yield mock

@pytest.fixture
def mock_hash_password():
    with patch("routes.user_routes.hash_password") as mock:
        yield mock

@pytest.fixture
def mock_create_access_token():
    with patch("routes.user_routes.create_access_token") as mock:
        yield mock

#@pytest.mark.usefixtures("mock_add_user", "mock_hash_password")
def test_register_success(mock_add_user, mock_hash_password):
    mock_add_user.return_value = UserResponse(username="test11@example.com", email="test11@example.com", role="user")
    mock_hash_password.return_value = "hashedpassword"

    response = client.post("/register", json={
        "email": "test11@example.com",
        "password": "testpassword"
    })

    assert response.status_code == 200
    assert response.json() == {
        "username": "test11@example.com",
        "email": "test11@example.com",
        "role": "user",
        "first_name": None,
        "last_name": None,
        "phone_number": None,
        "photo": None
    }


def test_register_user_exists(mock_add_user):
    mock_add_user.return_value = None

    response = client.post("/register", json={
        "email": "test@example.com",
        "password": "testpassword"
    })

    assert response.status_code == 400
    assert response.json() == {"detail": "Email already exists"}


def test_login_success(mock_get_user_for_authentication, mock_verify_password, mock_create_access_token):
    mock_get_user_for_authentication.return_value = UserLogin(email="test@example.com", password="hashedpassword", role="user", username="test@example.com")
    mock_verify_password.return_value = True
    mock_create_access_token.return_value = "fake_access_token"

    response = client.post("/login", json={
        "email": "test@example.com",
        "password": "testpassword"
    })

    assert response.status_code == 200
    assert response.json() == {
        "username": "test@example.com",
        "email": "test@example.com",
        "role": "user",
        "first_name": None,
        "last_name": None,
        "phone_number": None,
        "photo": None
    }

def test_login_invalid_credentials(mock_get_user_for_authentication, mock_verify_password):
    mock_get_user_for_authentication.return_value = None
    mock_verify_password.return_value = False

    response = client.post("/login", json={
        "email": "test@example.com",
        "password": "wrongpassword"
    })

    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid credentials"}

