import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app
from model.user_model import UserCreate, UserLogin, UserResponse, UserUpdate
from dependency.user_dependency import get_current_user

client = TestClient(app)

# ------------------------
#    Pytest Fixtures
# ------------------------
@pytest.fixture
def mock_get_user_profile():
    with patch("routes.user_routes.get_user_profile") as mock:
        yield mock

@pytest.fixture
def mock_get_user_for_authentication():
    with patch("routes.user_routes.get_user_for_authentication") as mock:
        yield mock

@pytest.fixture
def mock_add_user():
    with patch("routes.user_routes.add_user") as mock:
        yield mock

@pytest.fixture
def mock_update_user_info():
    with patch("routes.user_routes.update_user_info") as mock:
        yield mock

@pytest.fixture
def mock_hash_password():
    with patch("routes.user_routes.hash_password") as mock:
        yield mock

@pytest.fixture
def mock_verify_password():
    with patch("routes.user_routes.verify_password") as mock:
        yield mock

@pytest.fixture
def mock_create_access_token():
    with patch("routes.user_routes.create_access_token") as mock:
        yield mock

@pytest.fixture
def mock_create_refresh_token():
    with patch("routes.user_routes.create_refresh_token") as mock:
        yield mock

@pytest.fixture
def mock_verify_access_token():
    with patch("routes.user_routes.verify_access_token") as mock:
        yield mock

@pytest.fixture
def mock_verify_refresh_token():
    with patch("routes.user_routes.verify_refresh_token") as mock:
        yield mock

@pytest.fixture    
def mock_get_current_user():
    with patch("dependency.user_dependency.get_current_user") as mock:
        yield mock

# ------------------------------------------------
#               /register Endpoint
# ------------------------------------------------
def test_register_user_exists(mock_get_user_profile):
    # get_user_profile returns an existing user => 400
    mock_get_user_profile.return_value = UserResponse(username="existinguser", email="test@example.com", role="user")
    response = client.post("/register", json={"email": "test@example.com", "password": "password"})
    assert response.status_code == 400
    assert response.json() == {"detail": "User already exists"}

def test_register_create_user_failed(mock_get_user_profile, mock_add_user):
    # get_user_profile: no user => can create
    mock_get_user_profile.return_value = None
    # add_user returns None => 400
    mock_add_user.return_value = None
    response = client.post("/register", json={"email": "test2@example.com", "password": "password"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Failed to create user"}

def test_register_internal_error(mock_get_user_profile, mock_add_user):
    mock_get_user_profile.return_value = None
    mock_add_user.side_effect = Exception("DB error")
    response = client.post("/register", json={"email": "brandnew@example.com", "password": "password"})
    assert response.status_code == 500
    assert response.json() == {"detail": "Internal server error"}

def test_register_success(mock_get_user_profile, mock_add_user, mock_hash_password):
    mock_get_user_profile.return_value = None
    mock_add_user.return_value = UserResponse(username="testuser", email="test@example.com", role="user")
    mock_hash_password.return_value = "hashed"
    response = client.post("/register", json={"email": "test@example.com", "password": "password"})
    assert response.status_code == 200
    assert "user" in response.json()
    assert response.json()["user"]["username"] == "testuser"
    assert response.json()["user"]["email"] == "test@example.com"
    assert response.json()["user"]["role"] == "user"

# ------------------------------------------------
#                /login Endpoint
# ------------------------------------------------
def test_login_missing_fields():
    response = client.post("/login", json={})
    assert response.status_code == 422
    assert response.json() == {"detail": [
        {
            "type": "missing",
            "loc": [
                "body",
                "password"
            ],
            "msg": "Field required",
            "input": {}
        }
    ]}

def test_login_missing_password():
    response = client.post("/login", json={"username": "testuser"})
    assert response.status_code == 422
    assert response.json() == {"detail": [
        {
            "type": "missing",
            "loc": [
                "body",
                "password"
            ],
            "msg": "Field required",
            "input": {
                "username": "testuser"
            }
        }
    ]}

def test_login_missing_username_email_phone():
    response = client.post("/login", json={"password": "password"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Email, username or phone number is required"}

def test_login_invalid_credentials(mock_get_user_for_authentication, mock_verify_password):
    mock_get_user_for_authentication.return_value = UserLogin(username="testuser", email="nonexistent@example.com", password="password", role="user")
    mock_verify_password.return_value = False
    response = client.post("/login", json={"email": "nonexistent@example.com", "password": "password"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid credentials"}

def test_login_success(mock_get_user_for_authentication, mock_verify_password, mock_create_access_token, mock_create_refresh_token):
    user_db = UserLogin(username="testuser", email="test@example.com", password="password", role="user")
    mock_get_user_for_authentication.return_value = user_db
    mock_verify_password.return_value = True
    mock_create_access_token.return_value = "access_token"
    mock_create_refresh_token.return_value = "refresh_token"

    response = client.post("/login", json={"email": "test@example.com", "password": "password"})
    assert response.status_code == 200
    assert response.json()["access_token"] == "access_token"
    assert response.json()["user"]["username"] == "testuser"
    assert response.json()["user"]["email"] == "test@example.com"
    assert response.json()["user"]["role"] == "user"

# ------------------------------------------------
#             /verify-token Endpoint
# ------------------------------------------------
def test_verify_token_success(mock_verify_access_token, mock_get_user_for_authentication):
    mock_verify_access_token.return_value = {"sub": "test@example.com"}
    mock_get_user_for_authentication.return_value = UserResponse(username="testuser", email="test@example.com", role="user")
    response = client.get("/verify-token", headers={"Authorization": "Bearer access_token"})
    assert response.status_code == 200
    assert response.json()["user"]["username"] == "testuser"

def test_verify_token_missing_token():
    response = client.get("/verify-token")
    assert response.status_code == 401
    assert response.json() == {"detail": "Access token missing or invalid"}

def test_verify_token_invalid_token(mock_verify_access_token):
    mock_verify_access_token.return_value = None
    response = client.get("/verify-token", headers={"Authorization": "Bearer invalid"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid access token"}

def test_verify_token_user_not_found(mock_verify_access_token, mock_get_user_for_authentication):
    mock_verify_access_token.return_value = {"sub": "test@example.com"}
    mock_get_user_for_authentication.return_value = None
    response = client.get("/verify-token", headers={"Authorization": "Bearer access_token"})
    assert response.status_code == 401
    assert response.json() == {"detail": "User not found"}

# ------------------------------------------------
#             /refresh-token Endpoint
# ------------------------------------------------
def test_refresh_token_missing_token():
    response = client.get("/refresh-token")
    assert response.status_code == 401
    assert response.json() == {"detail": "Refresh token missing"}

def test_refresh_token_invalid_token(mock_verify_refresh_token):
    mock_verify_refresh_token.return_value = None
    response = client.get("/refresh-token", headers={"Cookie": "refresh_token=invalid"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid refresh token"}

def test_refresh_token_success(mock_verify_refresh_token, mock_get_user_for_authentication, mock_create_access_token, mock_create_refresh_token):
    mock_verify_refresh_token.return_value = {"sub": "test@example.com"}
    mock_get_user_for_authentication.return_value = UserResponse(
        username="testuser", email="test@example.com", role="user"
    )
    mock_create_access_token.return_value = "new_access_token"

    response = client.get("/refresh-token", headers={"Cookie": "refresh_token=valid"})
    assert response.status_code == 200
    assert response.json()["access_token"] == "new_access_token"

# ------------------------------------------------
#               /logout Endpoint
# ------------------------------------------------
def test_logout():
    response = client.get("/logout")
    assert response.status_code == 200
    assert response.json() == {"message": "Logged out successfully"}

# ------------------------------------------------
#            /update_user Endpoint
# ------------------------------------------------

async def mock_get_current_user():
    return UserResponse(username="testuser", email="old@example.com", role="user")

def test_update_user_success(mock_update_user_info):
    app.dependency_overrides[get_current_user] = mock_get_current_user

    # 模擬 update_user_info 的行為：將新數據應用於現有數據
    def mock_update_logic(current_user, user_update):
        updated_data = current_user.model_dump()  
        updated_data.update(user_update.model_dump()) 
        return UserResponse(**updated_data)
    
    mock_update_user_info.side_effect = mock_update_logic

    # 發送更新請求
    response = client.post(
        "/update_user",
        json={"username": "newuser", "first_name": "first", "last_name": "last", "phone_number": "1234567890"},
        headers={"Authorization": "Bearer access_token"}
    )

    app.dependency_overrides.clear()

    # 驗證返回結果是否正確反映更新
    assert response.status_code == 200
    result = response.json()["user"]
    assert result["username"] == "newuser"
    assert result["email"] == "old@example.com"  # 未更改的值仍然一致
    assert result["role"] == "user"
    assert result["first_name"] == "first"
    assert result["last_name"] == "last"
    assert result["phone_number"] == "1234567890"

def test_update_user_failed(mock_update_user_info):
    app.dependency_overrides[get_current_user] = mock_get_current_user
    
    # update_user_info returns the updated user
    mock_update_user_info.return_value = None

    response = client.post(
        "/update_user",
        json={"username": "newuser", "first_name": "first", "last_name": "last", "phone_number": "1234567890"},
        headers={"Authorization": "Bearer access_token"}
    )

    app.dependency_overrides.clear()

    assert response.status_code == 400
    assert response.json() == {"detail": "Failed to update user"}
