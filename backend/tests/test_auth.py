"""
Authentication tests for the Todo API.

This module tests the complete authentication flow including user registration,
login, token validation, and protected endpoint access.
"""
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select
from uuid import uuid4
from datetime import timedelta

from src.main import app
from src.models.user import User
from src.database.connection import sync_engine as engine
from src.auth.jwt_handler import create_access_token, verify_token


@pytest.fixture
def client():
    """Create a test client for the API."""
    with TestClient(app) as c:
        yield c


@pytest.fixture
def db_session():
    """Create a database session for testing."""
    from src.database.connection import get_sync_session

    # Use the generator approach similar to the actual dependency
    session_gen = get_sync_session()
    session = next(session_gen)
    yield session
    try:
        next(session_gen)
    except StopIteration:
        pass  # Expected behavior when closing the generator


def test_register_new_user(client: TestClient, db_session):
    """Test registering a new user."""
    # Clean up any existing user with this email
    email = f"testuser_{uuid4()}@example.com"

    user_data = {
        "email": email,
        "password": "SecurePass123!"
    }

    response = client.post("/api/auth/register", json=user_data)
    assert response.status_code == 200

    data = response.json()
    assert data["email"] == email
    assert "id" in data
    assert data["is_active"] is True


def test_register_existing_user(client: TestClient, db_session: Session):
    """Test registering a user that already exists."""
    # First register a user
    email = f"testuser2_{uuid4()}@example.com"
    user_data = {
        "email": email,
        "password": "SecurePass123!"
    }

    # Register the user
    response = client.post("/api/auth/register", json=user_data)
    assert response.status_code == 200

    # Try to register the same user again
    response = client.post("/api/auth/register", json=user_data)
    assert response.status_code == 409  # Conflict


def test_login_valid_credentials(client: TestClient, db_session: Session):
    """Test logging in with valid credentials."""
    # First register a user
    email = f"login_test_{uuid4()}@example.com"
    password = "SecurePass123!"

    user_data = {
        "email": email,
        "password": password
    }

    # Register the user
    response = client.post("/api/auth/register", json=user_data)
    assert response.status_code == 200

    # Login with valid credentials
    login_data = {
        "email": email,
        "password": password
    }

    response = client.post("/api/auth/login", json=login_data)
    assert response.status_code == 200

    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client: TestClient, db_session: Session):
    """Test logging in with invalid credentials."""
    # Try to login with non-existent user
    login_data = {
        "email": "nonexistent@example.com",
        "password": "wrongpassword"
    }

    response = client.post("/api/auth/login", json=login_data)
    assert response.status_code == 401


def test_get_current_user_with_valid_token(client: TestClient, db_session: Session):
    """Test getting current user info with a valid token."""
    # First register and login a user
    email = f"me_test_{uuid4()}@example.com"
    password = "SecurePass123!"

    user_data = {
        "email": email,
        "password": password
    }

    # Register the user
    response = client.post("/api/auth/register", json=user_data)
    assert response.status_code == 200

    # Login to get token
    login_data = {
        "email": email,
        "password": password
    }

    response = client.post("/api/auth/login", json=login_data)
    assert response.status_code == 200

    token_data = response.json()
    access_token = token_data["access_token"]

    # Get current user info with valid token
    response = client.get("/api/auth/me",
                         headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200

    user_data = response.json()
    assert user_data["email"] == email


def test_protected_endpoint_without_token(client: TestClient):
    """Test accessing a protected endpoint without a token."""
    response = client.get("/api/auth/me")
    assert response.status_code == 401


def test_weak_password_validation(client: TestClient):
    """Test that weak passwords are rejected."""
    email = f"weak_pass_{uuid4()}@example.com"

    # Test with a password that's too short
    user_data = {
        "email": email,
        "password": "short"
    }

    response = client.post("/api/auth/register", json=user_data)
    assert response.status_code == 400

    # Test with a password missing uppercase
    user_data = {
        "email": email,
        "password": "alllowercase123"
    }

    response = client.post("/api/auth/register", json=user_data)
    assert response.status_code == 400

    # Test with a password missing lowercase
    user_data = {
        "email": email,
        "password": "ALLUPPERCASE123"
    }

    response = client.post("/api/auth/register", json=user_data)
    assert response.status_code == 400

    # Test with a password missing digits
    user_data = {
        "email": email,
        "password": "NoDigitsHere"
    }

    response = client.post("/api/auth/register", json=user_data)
    assert response.status_code == 400


def test_jwt_token_creation():
    """Test JWT token creation."""
    token_data = {"user_id": "test_user_123"}
    token = create_access_token(token_data)

    # Verify the token can be decoded
    decoded = verify_token(token)
    assert decoded is not None
    assert decoded.user_id == "test_user_123"


def test_jwt_token_expiration():
    """Test JWT token expiration."""
    # Create a token that expires immediately
    token_data = {"user_id": "test_user_123"}
    expired_token = create_access_token(token_data, expires_delta=timedelta(seconds=-1))

    # Verify the expired token cannot be decoded
    decoded = verify_token(expired_token)
    assert decoded is None


def test_jwt_token_verification_with_valid_token():
    """Test JWT token verification with a valid token."""
    token_data = {"user_id": "valid_user_456"}
    token = create_access_token(token_data)

    decoded = verify_token(token)
    assert decoded is not None
    assert decoded.user_id == "valid_user_456"


def test_protected_v2_endpoint_requires_valid_token(client):
    """Test that a protected v2 endpoint requires a valid token."""
    # Try to access a protected endpoint without a token
    response = client.get("/api/v2/users/test_user_123/tasks")

    assert response.status_code == 401
    assert "WWW-Authenticate" in response.headers


def test_protected_v2_endpoint_accepts_valid_token(client):
    """Test that a protected v2 endpoint accepts a valid token."""
    # Create a valid token
    token_data = {"user_id": "test_user_123"}
    token = create_access_token(token_data)

    headers = {"Authorization": f"Bearer {token}"}

    # Try to access a protected endpoint with a valid token
    response = client.get("/api/v2/users/test_user_123/tasks", headers=headers)

    # Should return 200 (OK) but empty list since user has no tasks
    assert response.status_code == 200


def test_protected_v2_endpoint_rejects_expired_token(client):
    """Test that a protected v2 endpoint rejects an expired token."""
    # Create an expired token
    token_data = {"user_id": "expired_user_789"}
    expired_token = create_access_token(token_data, expires_delta=timedelta(seconds=-1))

    headers = {"Authorization": f"Bearer {expired_token}"}

    # Try to access a protected endpoint with an expired token
    response = client.get("/api/v2/users/expired_user_789/tasks", headers=headers)

    assert response.status_code == 401


def test_jwt_payload_structure():
    """Test that JWT tokens have the expected payload structure."""
    import jwt
    from src.config.settings import settings

    token_data = {"user_id": "payload_user_111"}
    token = create_access_token(token_data)

    # Decode without verification to check structure
    payload = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"], options={"verify_signature": False})

    assert "exp" in payload
    assert "iat" in payload
    assert "user_id" in payload
    assert payload["user_id"] == "payload_user_111"