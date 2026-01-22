"""
Test database setup for in-memory SQLite database.
"""
from sqlmodel import create_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy import select
from contextlib import asynccontextmanager
from unittest.mock import AsyncMock, MagicMock
import asyncio
from src.models.todo import SQLModel, Todo
from src.models.todo import TodoCreate, TodoUpdate


def create_test_engine():
    """Create an in-memory SQLite engine for testing."""
    # Use in-memory SQLite database for testing
    sqlite_url = "sqlite+aiosqlite:///:memory:"
    engine = create_async_engine(
        sqlite_url,
        echo=False,
        poolclass=StaticPool,  # Use static pool for in-memory database
        connect_args={"check_same_thread": False}  # Required for SQLite in-memory
    )
    return engine


def create_test_sessionmaker(async_engine):
    """Create a test session maker."""
    return async_sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=async_engine,
        class_=AsyncSession
    )


async def create_test_db_and_tables(async_engine):
    """Create test database tables."""
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


def override_get_async_session(async_sessionmaker):
    """Override function for dependency injection."""
    async def get_async_session():
        async with async_sessionmaker() as session:
            yield session
    return get_async_session


# Mock database functions for testing
async def mock_get_all_todos(session: AsyncSession, offset: int = 0, limit: int = 100):
    """Mock function to get all todos."""
    statement = select(Todo).offset(offset).limit(limit)
    result = await session.execute(statement)
    return result.scalars().all()


async def mock_get_todo_by_id(session: AsyncSession, todo_id: int):
    """Mock function to get a todo by ID."""
    statement = select(Todo).where(Todo.id == todo_id)
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def mock_create_todo(session: AsyncSession, todo_data):
    """Mock function to create a todo."""
    # Convert Pydantic model to dict properly for SQLModel
    if hasattr(todo_data, 'model_dump'):
        todo_dict = todo_data.model_dump()
    elif hasattr(todo_data, 'dict'):
        todo_dict = todo_data.dict()
    else:
        # Assume it's already a dict
        todo_dict = todo_data

    db_todo = Todo(**todo_dict)
    session.add(db_todo)
    await session.commit()
    await session.refresh(db_todo)
    return db_todo


async def mock_update_todo(session: AsyncSession, todo_id: int, todo_data):
    """Mock function to update a todo."""
    statement = select(Todo).where(Todo.id == todo_id)
    result = await session.execute(statement)
    db_todo = result.scalar_one_or_none()

    if db_todo:
        # Update fields based on provided data
        # Convert Pydantic model to dict properly
        if hasattr(todo_data, 'model_dump'):
            update_data = todo_data.model_dump(exclude_unset=True)
        elif hasattr(todo_data, 'dict'):
            update_data = todo_data.dict(exclude_unset=True)
        else:
            # Assume it's already a dict
            update_data = todo_data

        for field, value in update_data.items():
            setattr(db_todo, field, value)

        await session.commit()
        await session.refresh(db_todo)
        return db_todo
    return None


async def mock_delete_todo(session: AsyncSession, todo_id: int):
    """Mock function to delete a todo."""
    statement = select(Todo).where(Todo.id == todo_id)
    result = await session.execute(statement)
    db_todo = result.scalar_one_or_none()

    if db_todo:
        await session.delete(db_todo)
        await session.commit()
        return True
    return False