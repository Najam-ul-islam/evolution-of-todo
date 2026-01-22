"""
Test fixtures for authenticated users.

This module provides pytest fixtures for testing authenticated user scenarios.
"""
import pytest
import pytest_asyncio
from datetime import timedelta
from src.auth.jwt_handler import create_access_token
import asyncio
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import StaticPool
from src.config.settings import settings
from .test_database_setup import create_test_engine, create_test_sessionmaker, create_test_db_and_tables, override_get_async_session
from unittest.mock import patch
from src.main import app


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


@pytest_asyncio.fixture
async def async_db_session():
    """Create an async database session for testing."""
    async with AsyncSessionFactory() as session:
        try:
            yield session
        finally:
            await session.close()


# Global test engine and sessionmaker for all tests
_test_async_engine = None
_test_async_sessionmaker = None


@pytest_asyncio.fixture(scope="session")
async def test_database():
    """Setup test database with in-memory SQLite."""
    global _test_async_engine, _test_async_sessionmaker

    # Create test engine and sessionmaker
    _test_async_engine = create_test_engine()
    _test_async_sessionmaker = create_test_sessionmaker(_test_async_engine)

    # Create tables
    await create_test_db_and_tables(_test_async_engine)

    yield _test_async_sessionmaker

    # Cleanup
    await _test_async_engine.dispose()


@pytest_asyncio.fixture
async def async_db_session(test_database):
    """Create an async database session for testing."""
    async with _test_async_sessionmaker() as session:
        try:
            yield session
        finally:
            await session.close()


@pytest_asyncio.fixture
async def clean_db_session(test_database):
    """Create a clean async database session that rolls back changes."""
    async with _test_async_sessionmaker() as session:
        try:
            yield session
        finally:
            # Rollback any changes to keep the database clean for other tests
            await session.rollback()
            await session.close()


@pytest_asyncio.fixture(scope="function")
async def db_session(test_database):
    """Create a database session that gets rolled back after each test."""
    async with _test_async_sessionmaker() as session:
        try:
            # Begin a transaction
            await session.begin()
            yield session
            # Rollback the transaction to clean up
            await session.rollback()
        except Exception as e:
            # Rollback on exception
            await session.rollback()
            raise
        finally:
            await session.close()


@pytest.fixture(autouse=True)
def override_dependencies(db_session):
    """Override dependencies for all tests."""
    from src.database.connection import get_async_session

    # Create a wrapper that returns the same session for the duration of the test
    async def get_test_session():
        yield db_session

    # Override the get_async_session dependency
    app.dependency_overrides[get_async_session] = get_test_session

    yield  # Run the test

    # Clean up the dependency override after the test
    app.dependency_overrides.clear()


@pytest.fixture
def client():
    """Create a test client."""
    from fastapi.testclient import TestClient
    with TestClient(app) as test_client:
        yield test_client