"""
Database integration tests for the Todo application.

This module tests the database connectivity and persistence functionality.
"""
import pytest
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.database.connection import AsyncSessionFactory
from src.models.todo import Todo
from src.services.todo_service import TodoService


@pytest.mark.asyncio
async def test_database_connection():
    """Test that we can establish a database connection."""
    async with AsyncSessionFactory() as session:
        assert isinstance(session, AsyncSession)
        # Execute a simple query to verify the connection
        result = await session.exec(select(Todo).limit(1))
        # No assertion needed - if we get here, connection worked


@pytest.mark.asyncio
async def test_create_todo_persistence():
    """Test that todos can be created and persisted."""
    async with AsyncSessionFactory() as session:
        # Create a test todo
        test_todo = Todo(
            title="Test Todo for Persistence",
            description="This is a test todo to verify persistence",
            completed=False,
            user_id="test_user_db_integration"
        )

        session.add(test_todo)
        await session.commit()
        await session.refresh(test_todo)

        assert test_todo.id is not None
        assert test_todo.title == "Test Todo for Persistence"
        assert test_todo.user_id == "test_user_db_integration"

        # Clean up
        await session.delete(test_todo)
        await session.commit()


@pytest.mark.asyncio
async def test_todo_service_create():
    """Test TodoService create functionality."""
    async with AsyncSessionFactory() as session:
        from src.models.todo import TodoCreate

        todo_create = TodoCreate(
            title="Service Test Todo",
            description="Todo created via TodoService",
            completed=False
        )

        created_todo = await TodoService.create_todo(session, "test_user_service", todo_create)

        assert created_todo.id is not None
        assert created_todo.title == "Service Test Todo"
        assert created_todo.user_id == "test_user_service"

        # Clean up
        await session.delete(created_todo)
        await session.commit()


@pytest.mark.asyncio
async def test_todo_service_user_isolation():
    """Test that TodoService enforces user isolation."""
    async with AsyncSessionFactory() as session:
        from src.models.todo import TodoCreate

        # Create todos for different users
        todo_user1 = TodoCreate(
            title="User 1 Todo",
            description="Todo for user 1",
            completed=False
        )

        todo_user2 = TodoCreate(
            title="User 2 Todo",
            description="Todo for user 2",
            completed=False
        )

        # Create todos for different users
        created_todo1 = await TodoService.create_todo(session, "user_1", todo_user1)
        created_todo2 = await TodoService.create_todo(session, "user_2", todo_user2)

        # Verify each user can only see their own todos
        user1_todos = await TodoService.get_todos_by_user(session, "user_1")
        user2_todos = await TodoService.get_todos_by_user(session, "user_2")

        assert len(user1_todos) == 1
        assert user1_todos[0].title == "User 1 Todo"
        assert user1_todos[0].user_id == "user_1"

        assert len(user2_todos) == 1
        assert user2_todos[0].title == "User 2 Todo"
        assert user2_todos[0].user_id == "user_2"

        # Verify user 1 cannot access user 2's todo
        user1_access_to_user2_todo = await TodoService.get_todo_by_id(
            session, "user_1", created_todo2.id
        )
        assert user1_access_to_user2_todo is None

        # Verify user 2 cannot access user 1's todo
        user2_access_to_user1_todo = await TodoService.get_todo_by_id(
            session, "user_2", created_todo1.id
        )
        assert user2_access_to_user1_todo is None

        # Clean up
        await session.delete(created_todo1)
        await session.delete(created_todo2)
        await session.commit()


@pytest.mark.asyncio
async def test_todo_service_crud_operations():
    """Test all CRUD operations in TodoService."""
    async with AsyncSessionFactory() as session:
        from src.models.todo import TodoCreate, TodoUpdate

        # Create a todo
        todo_create = TodoCreate(
            title="CRUD Test Todo",
            description="Todo for testing CRUD operations",
            completed=False
        )

        created_todo = await TodoService.create_todo(session, "crud_test_user", todo_create)
        assert created_todo.title == "CRUD Test Todo"

        # Read the todo
        retrieved_todo = await TodoService.get_todo_by_id(
            session, "crud_test_user", created_todo.id
        )
        assert retrieved_todo is not None
        assert retrieved_todo.title == "CRUD Test Todo"

        # Update the todo
        todo_update = TodoUpdate(
            title="Updated CRUD Test Todo",
            completed=True
        )

        updated_todo = await TodoService.update_todo(
            session, "crud_test_user", created_todo.id, todo_update
        )
        assert updated_todo is not None
        assert updated_todo.title == "Updated CRUD Test Todo"
        assert updated_todo.completed is True

        # Toggle completion status
        toggled_todo = await TodoService.toggle_completion(
            session, "crud_test_user", created_todo.id
        )
        assert toggled_todo is not None
        assert toggled_todo.completed is False  # Should be toggled back to False

        # Delete the todo
        delete_result = await TodoService.delete_todo(
            session, "crud_test_user", created_todo.id
        )
        assert delete_result is True

        # Verify deletion
        deleted_todo = await TodoService.get_todo_by_id(
            session, "crud_test_user", created_todo.id
        )
        assert deleted_todo is None


@pytest.mark.asyncio
async def test_todo_service_nonexistent_todo():
    """Test TodoService behavior with nonexistent todos."""
    async with AsyncSessionFactory() as session:
        from src.models.todo import TodoUpdate

        # Try to get a non-existent todo
        nonexistent_todo = await TodoService.get_todo_by_id(
            session, "test_user", 999999
        )
        assert nonexistent_todo is None

        # Try to update a non-existent todo
        todo_update = TodoUpdate(title="Should not update")
        updated_todo = await TodoService.update_todo(
            session, "test_user", 999999, todo_update
        )
        assert updated_todo is None

        # Try to delete a non-existent todo
        delete_result = await TodoService.delete_todo(
            session, "test_user", 999999
        )
        assert delete_result is False

        # Try to toggle completion of a non-existent todo
        toggled_todo = await TodoService.toggle_completion(
            session, "test_user", 999999
        )
        assert toggled_todo is None