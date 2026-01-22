"""
Database connection utilities for the Todo application.

This module provides database connection management using SQLModel and asyncpg
for PostgreSQL connectivity.
"""
from typing import AsyncGenerator
from sqlmodel import create_engine, Session
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
import asyncio

from ..config.settings import settings


# Create async engine for PostgreSQL with asyncpg driver
async_engine = create_async_engine(
    settings.database_url,  # Use the full URL with asyncpg for async operations
    echo=False,  # Set to True for SQL query logging
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300,  # Recycle connections after 5 minutes
    pool_size=10,  # Number of connection pools (increased for better performance)
    max_overflow=20,  # Additional connections beyond pool_size (increased for better performance)
    pool_timeout=30,  # Seconds to wait before giving up on getting a connection
    pool_reset_on_return="commit",  # Reset connections when returned to pool
    poolclass=None,  # Use default async pool class
)


# Create async session maker
AsyncSessionFactory = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession
)


# Create sync engine for migration support
sync_engine = create_engine(
    settings.database_url.replace("asyncpg", "psycopg2"),  # Replace asyncpg with psycopg2 for sync operations
    echo=False,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=10,  # Increased for better performance
    max_overflow=20,  # Increased for better performance
    pool_timeout=30,
    pool_reset_on_return="commit",  # Reset connections when returned to pool
)


def create_db_and_tables():
    """
    Create database tables based on SQLModel models.

    This function creates all tables defined in the SQLModel metadata.
    """
    from ..models.todo import SQLModel  # Import here to avoid circular imports

    # Create all tables synchronously
    SQLModel.metadata.create_all(bind=sync_engine)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Get an async database session.

    Yields:
        AsyncSession: An asynchronous database session
    """
    async with AsyncSessionFactory() as session:
        try:
            yield session
        finally:
            await session.close()


def get_sync_session() -> Session:
    """
    Get a synchronous database session.

    Returns:
        Session: A synchronous database session
    """
    from ..models.todo import SQLModel  # Import here to avoid circular imports

    with Session(sync_engine) as session:
        yield session


async def close_async_engine():
    """
    Close the async engine and all its connections.
    """
    await async_engine.dispose()


def validate_database_connection():
    """
    Validate the database connection by attempting to connect.

    Returns:
        bool: True if connection is successful, False otherwise
    """
    from sqlalchemy import text
    try:
        # Try to create a simple connection
        with Session(sync_engine) as session:
            # Execute a simple query to test connection
            session.execute(text("SELECT 1"))
        return True
    except Exception as e:
        print(f"Database connection validation failed: {e}")
        return False


async def validate_async_database_connection():
    """
    Validate the async database connection by attempting to connect.

    Returns:
        bool: True if connection is successful, False otherwise
    """
    from sqlmodel import text
    try:
        async with AsyncSessionFactory() as session:
            # Execute a simple query to test connection
            result = await session.exec(text("SELECT 1"))
        return True
    except Exception as e:
        print(f"Async database connection validation failed: {e}")
        return False