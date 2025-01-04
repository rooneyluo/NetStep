import pytest
from fastapi.testclient import TestClient
from backend.main import app  # Assuming your FastAPI app is defined in main.py
from backend.model.user_model import UserCreate, UserLogin
from unittest.mock import patch

client = TestClient(app)

@pytest.fixture
def mock_add_user():
    with patch("backend.routes.user_routes.add_user") as mock:
        yield mock

@pytest.fixture
def mock_get_user_by_username_or_email():
    with patch("backend.routes.user_routes.get_user_by_username_or_email") as mock:
        yield mock

@pytest.fixture
def mock_verify_password():
    with patch("backend.routes.user_routes.verify_password") as mock:
        yield mock

@pytest.fixture
def mock_hash_password():
    with patch("backend.routes.user_routes.hash_password") as mock:
        yield mock

@pytest.fixture
def mock_create_access_token():
    with patch("backend.routes.user_routes.create_access_token") as mock:
        yield mock

def test_register_success(mock_add_user, mock_hash_password, mock_create_access_token):
    mock_add_user.return_value = UserCreate(username="testuser", email="test@example.com", password="hashedpassword")
    mock_hash_password.return_value = "hashedpassword"
    mock_create_access_token.return_value = "fake_access_token"

    response = client.post("/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword"
    })

    assert response.status_code == 200
    assert response.json() == {
        "username": "testuser",
        "email": "test@example.com"
    }

def test_register_user_exists(mock_add_user):
    mock_add_user.return_value = None

    response = client.post("/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword"
    })

    assert response.status_code == 400
    assert response.json() == {"detail": "User already exists"}

def test_login_success(mock_get_user_by_username_or_email, mock_verify_password, mock_create_access_token):
    mock_get_user_by_username_or_email.return_value = UserLogin(username="testuser", email="test@example.com", password="hashedpassword")
    mock_verify_password.return_value = True
    mock_create_access_token.return_value = "fake_access_token"

    response = client.post("/login", json={
        "email": "test@example.com",
        "password": "testpassword"
    })

    assert response.status_code == 200
    assert response.json() == {
        "username": "testuser",
        "email": "test@example.com"
    }

def test_login_invalid_credentials(mock_get_user_by_username_or_email, mock_verify_password):
    mock_get_user_by_username_or_email.return_value = None
    mock_verify_password.return_value = False

    response = client.post("/login", json={
        "email": "test@example.com",
        "password": "wrongpassword"
    })

    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid credentials"}