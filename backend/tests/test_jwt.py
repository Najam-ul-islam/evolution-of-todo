"""
JWT-specific tests for the Todo API.

This module tests JWT token creation, validation, and refresh functionality.
"""
import pytest
from fastapi.testclient import TestClient
from datetime import timedelta
import jwt

from src.main import app
from src.auth.jwt_handler import (
    create_access_token,
    create_refresh_token,
    verify_token,
    verify_refresh_token
)
from src.config.settings import settings


@pytest.fixture
def client():
    """Create a test client for the API."""
    with TestClient(app) as c:
        yield c


def test_access_token_creation():
    """Test access token creation."""
    token_data = {"user_id": "test_user_123"}
    token = create_access_token(token_data)

    # Verify the token can be decoded
    decoded = verify_token(token)
    assert decoded is not None
    assert decoded.user_id == "test_user_123"


def test_refresh_token_creation():
    """Test refresh token creation."""
    token_data = {"user_id": "test_user_123"}
    token = create_refresh_token(token_data)

    # Verify the refresh token can be decoded
    decoded = verify_refresh_token(token)
    assert decoded is not None
    assert decoded.user_id == "test_user_123"


def test_access_token_expiration():
    """Test access token expiration."""
    # Create a token that expires immediately
    token_data = {"user_id": "test_user_123"}
    expired_token = create_access_token(token_data, expires_delta=timedelta(seconds=-1))

    # Verify the expired token cannot be decoded
    decoded = verify_token(expired_token)
    assert decoded is None


def test_refresh_token_expiration():
    """Test refresh token expiration."""
    # Create a token that expires immediately
    token_data = {"user_id": "test_user_123"}
    expired_token = create_refresh_token(token_data, expires_delta=timedelta(seconds=-1))

    # Verify the expired token cannot be decoded
    decoded = verify_refresh_token(expired_token)
    assert decoded is None


def test_access_token_verification_with_valid_token():
    """Test access token verification with a valid token."""
    token_data = {"user_id": "valid_user_456"}
    token = create_access_token(token_data)

    decoded = verify_token(token)
    assert decoded is not None
    assert decoded.user_id == "valid_user_456"


def test_refresh_token_verification_with_valid_token():
    """Test refresh token verification with a valid token."""
    token_data = {"user_id": "valid_user_456"}
    token = create_refresh_token(token_data)

    decoded = verify_refresh_token(token)
    assert decoded is not None
    assert decoded.user_id == "valid_user_456"


def test_access_token_cannot_verify_refresh_token():
    """Test that an access token verification function cannot verify a refresh token."""
    token_data = {"user_id": "test_user_123"}
    refresh_token = create_refresh_token(token_data)

    # Try to verify refresh token with access token verification function
    decoded = verify_token(refresh_token)
    assert decoded is None


def test_refresh_token_cannot_verify_access_token():
    """Test that a refresh token verification function cannot verify an access token."""
    token_data = {"user_id": "test_user_123"}
    access_token = create_access_token(token_data)

    # Try to verify access token with refresh token verification function
    decoded = verify_refresh_token(access_token)
    assert decoded is None


def test_access_token_payload_structure():
    """Test that access tokens have the expected payload structure."""
    token_data = {"user_id": "payload_user_111"}
    token = create_access_token(token_data)

    # Decode without verification to check structure
    payload = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"], options={"verify_signature": False})

    assert "exp" in payload
    assert "iat" in payload
    assert "user_id" in payload
    assert payload["user_id"] == "payload_user_111"


def test_refresh_token_payload_structure():
    """Test that refresh tokens have the expected payload structure."""
    token_data = {"user_id": "payload_user_111"}
    token = create_refresh_token(token_data)

    # Decode without verification to check structure
    payload = jwt.decode(token, settings.jwt_secret, algorithms=["HS256"], options={"verify_signature": False})

    assert "exp" in payload
    assert "iat" in payload
    assert "user_id" in payload
    assert "type" in payload
    assert payload["user_id"] == "payload_user_111"
    assert payload["type"] == "refresh"


def test_different_expiration_times():
    """Test that access and refresh tokens have different expiration times."""
    import time

    token_data = {"user_id": "exp_test_user"}

    # Create both tokens
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    # Decode both tokens to check expiration
    access_payload = jwt.decode(access_token, settings.jwt_secret, algorithms=["HS256"], options={"verify_signature": False})
    refresh_payload = jwt.decode(refresh_token, settings.jwt_secret, algorithms=["HS256"], options={"verify_signature": False})

    # Refresh token should have a longer expiration than access token
    access_exp = access_payload["exp"]
    refresh_exp = refresh_payload["exp"]

    # The difference should be significant (access token is 60 minutes, refresh token is 24 hours)
    assert refresh_exp > access_exp


def test_token_with_additional_claims():
    """Test token creation with additional claims."""
    token_data = {
        "user_id": "extra_claims_user",
        "role": "admin",
        "permissions": ["read", "write"]
    }

    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)

    # Verify access token contains additional claims
    access_decoded = verify_token(access_token)
    assert access_decoded is not None
    assert access_decoded.user_id == "extra_claims_user"

    # For refresh token, we need to manually decode to check additional claims
    refresh_payload = jwt.decode(refresh_token, settings.jwt_secret, algorithms=["HS256"], options={"verify_signature": False})
    assert refresh_payload["user_id"] == "extra_claims_user"
    assert refresh_payload["role"] == "admin"
    assert "read" in refresh_payload["permissions"]
    assert "write" in refresh_payload["permissions"]


def test_token_verification_fails_with_wrong_secret():
    """Test that token verification fails with wrong secret."""
    # Create a token with the correct secret
    token_data = {"user_id": "wrong_secret_test"}
    correct_token = create_access_token(token_data)

    # Try to decode with a wrong secret
    with pytest.raises(jwt.InvalidSignatureError):
        jwt.decode(correct_token, "wrong_secret", algorithms=["HS256"])


def test_token_with_empty_user_id():
    """Test token creation and verification with empty user_id."""
    token_data = {"user_id": ""}

    token = create_access_token(token_data)
    decoded = verify_token(token)

    # Empty user_id should still be valid as far as JWT verification goes
    # but the application logic might reject it
    assert decoded is not None
    assert decoded.user_id == ""


def test_token_with_none_user_id():
    """Test token creation with None user_id."""
    token_data = {"user_id": None}

    token = create_access_token(token_data)
    decoded = verify_token(token)

    # None user_id should be handled gracefully
    assert decoded is not None
    assert decoded.user_id is None