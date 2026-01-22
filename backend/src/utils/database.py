from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from typing import AsyncGenerator, Generator
import asyncio

from ..config.settings import settings


# Sync engine and session
sync_engine = create_engine(settings.database_url.replace("+asyncpg", ""))

def create_db_and_tables():
    """Create database tables"""
    SQLModel.metadata.create_all(sync_engine)


def get_sync_session() -> Generator[Session, None, None]:
    """Get a sync database session"""
    with Session(sync_engine) as session:
        yield session


async def validate_database_connection():
    """Validate that we can connect to the database"""
    try:
        async with async_engine.connect() as conn:
            # This will raise an exception if connection fails
            await conn.execute("SELECT 1")
        print("Database connection validated successfully")
        return True
    except Exception as e:
        print(f"Database connection validation failed: {e}")
        return False


# Async engine and session for async operations
async_engine = create_async_engine(settings.database_url)

AsyncSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine,
    class_=AsyncSession
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


# Context managers for easier session handling
class DatabaseSessionManager:
    def __init__(self):
        self.async_session = AsyncSessionLocal

    async def get_session(self):
        async with self.async_session() as session:
            yield session


# Utility functions for database operations
async def get_todo_by_id(session: AsyncSession, todo_id: int):
    """Get a todo by its ID"""
    from ..models.todo import Todo
    statement = select(Todo).where(Todo.id == todo_id)
    result = await session.execute(statement)
    return result.scalar_one_or_none()


async def get_all_todos(session: AsyncSession, offset: int = 0, limit: int = 100):
    """Get all todos with pagination"""
    from ..models.todo import Todo
    statement = select(Todo).offset(offset).limit(limit)
    result = await session.execute(statement)
    return result.scalars().all()


async def create_todo(session: AsyncSession, todo_data):
    """Create a new todo"""
    from ..models.todo import Todo
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


async def update_todo(session: AsyncSession, todo_id: int, todo_data):
    """Update a todo"""
    from ..models.todo import Todo
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


async def delete_todo(session: AsyncSession, todo_id: int):
    """Delete a todo"""
    from ..models.todo import Todo
    statement = select(Todo).where(Todo.id == todo_id)
    result = await session.execute(statement)
    db_todo = result.scalar_one_or_none()

    if db_todo:
        await session.delete(db_todo)
        await session.commit()
        return True
    return False


# Import select from SQLAlchemy
from sqlalchemy import select