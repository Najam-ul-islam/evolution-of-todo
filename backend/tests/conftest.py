"""
Test fixtures for authenticated users.

This module provides pytest fixtures for testing authenticated user scenarios.
"""
import pytest
from datetime import timedelta
from src.auth.jwt_handler import create_access_token


@pytest.fixture
def valid_user_token():
    """Create a valid JWT token for testing."""
    token_data = {"sub": "testuser", "user_id": "test_user_123"}
    return create_access_token(token_data, expires_delta=timedelta(hours=1))


@pytest.fixture
def another_user_token():
    """Create a JWT token for a different user for testing isolation."""
    token_data = {"sub": "anotheruser", "user_id": "another_user_456"}
    return create_access_token(token_data, expires_delta=timedelta(hours=1))


@pytest.fixture
def expired_token():
    """Create an expired JWT token for testing."""
    token_data = {"sub": "expireduser", "user_id": "expired_user_789"}
    return create_access_token(token_data, expires_delta=timedelta(seconds=-1))