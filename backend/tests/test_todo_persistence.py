"""
Todo persistence tests for the Todo application.

This module tests the persistent storage functionality and data validation.
"""
import pytest
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
import asyncio

from src.database.connection import AsyncSessionFactory
from src.models.todo import Todo
from src.services.todo_service import TodoService


@pytest.mark.asyncio
async def test_todo_persistence_across_sessions():
    """Test that todos persist across different database sessions."""
    # Create a todo in one session
    async with AsyncSessionFactory() as session:
        test_todo = Todo(
            title="Persistence Test Todo",
            description="This should persist across sessions",
            completed=False,
            user_id="test_user_persistence"
        )

        session.add(test_todo)
        await session.commit()
        await session.refresh(test_todo)

        todo_id = test_todo.id
        assert todo_id is not None

    # Verify the todo exists in a new session
    async with AsyncSessionFactory() as session:
        statement = select(Todo).where(Todo.id == todo_id)
        result = await session.exec(statement)
        retrieved_todo = result.first()

        assert retrieved_todo is not None
        assert retrieved_todo.title == "Persistence Test Todo"
        assert retrieved_todo.user_id == "test_user_persistence"

    # Clean up in another session
    async with AsyncSessionFactory() as session:
        statement = select(Todo).where(Todo.id == todo_id)
        result = await session.exec(statement)
        todo_to_delete = result.first()

        if todo_to_delete:
            await session.delete(todo_to_delete)
            await session.commit()


@pytest.mark.asyncio
async def test_multiple_todos_persistence():
    """Test that multiple todos can be stored and retrieved."""
    todo_ids = []

    # Create multiple todos
    async with AsyncSessionFactory() as session:
        for i in range(3):
            test_todo = Todo(
                title=f"Multi-Todo Test {i}",
                description=f"Description for todo {i}",
                completed=(i % 2 == 0),  # Alternate completed status
                user_id="test_user_multi"
            )

            session.add(test_todo)
            await session.commit()
            await session.refresh(test_todo)
            todo_ids.append(test_todo.id)

    # Verify all todos exist
    async with AsyncSessionFactory() as session:
        statement = select(Todo).where(Todo.user_id == "test_user_multi")
        result = await session.exec(statement)
        retrieved_todos = result.all()

        assert len(retrieved_todos) == 3

        titles = {todo.title for todo in retrieved_todos}
        expected_titles = {"Multi-Todo Test 0", "Multi-Todo Test 1", "Multi-Todo Test 2"}
        assert titles == expected_titles

    # Clean up
    async with AsyncSessionFactory() as session:
        for todo_id in todo_ids:
            statement = select(Todo).where(Todo.id == todo_id)
            result = await session.exec(statement)
            todo = result.first()
            if todo:
                await session.delete(todo)
        await session.commit()


@pytest.mark.asyncio
async def test_todo_field_persistence():
    """Test that all fields of a Todo are properly persisted."""
    async with AsyncSessionFactory() as session:
        original_todo = Todo(
            title="Field Persistence Test",
            description="Testing all fields are saved properly",
            completed=True,
            user_id="test_user_fields"
        )

        session.add(original_todo)
        await session.commit()
        await session.refresh(original_todo)

        original_id = original_todo.id
        assert original_id is not None

    # Retrieve and verify all fields
    async with AsyncSessionFactory() as session:
        statement = select(Todo).where(Todo.id == original_id)
        result = await session.exec(statement)
        retrieved_todo = result.first()

        assert retrieved_todo is not None
        assert retrieved_todo.id == original_id
        assert retrieved_todo.title == "Field Persistence Test"
        assert retrieved_todo.description == "Testing all fields are saved properly"
        assert retrieved_todo.completed is True
        assert retrieved_todo.user_id == "test_user_fields"
        assert retrieved_todo.created_at is not None
        assert retrieved_todo.updated_at is not None

    # Clean up
    async with AsyncSessionFactory() as session:
        statement = select(Todo).where(Todo.id == original_id)
        result = await session.exec(statement)
        todo = result.first()
        if todo:
            await session.delete(todo)
            await session.commit()


@pytest.mark.asyncio
async def test_todo_update_persistence():
    """Test that todo updates are properly persisted."""
    async with AsyncSessionFactory() as session:
        # Create initial todo
        test_todo = Todo(
            title="Original Title",
            description="Original Description",
            completed=False,
            user_id="test_user_update"
        )

        session.add(test_todo)
        await session.commit()
        await session.refresh(test_todo)

        original_id = test_todo.id
        assert original_id is not None

        # Update the todo
        test_todo.title = "Updated Title"
        test_todo.description = "Updated Description"
        test_todo.completed = True
        await session.commit()

    # Verify the update was persisted
    async with AsyncSessionFactory() as session:
        statement = select(Todo).where(Todo.id == original_id)
        result = await session.exec(statement)
        updated_todo = result.first()

        assert updated_todo is not None
        assert updated_todo.title == "Updated Title"
        assert updated_todo.description == "Updated Description"
        assert updated_todo.completed is True

    # Clean up
    async with AsyncSessionFactory() as session:
        statement = select(Todo).where(Todo.id == original_id)
        result = await session.exec(statement)
        todo = result.first()
        if todo:
            await session.delete(todo)
            await session.commit()


@pytest.mark.asyncio
async def test_todo_deletion_persistence():
    """Test that todo deletion is properly persisted."""
    async with AsyncSessionFactory() as session:
        # Create a todo
        test_todo = Todo(
            title="Deletion Test Todo",
            description="This will be deleted",
            completed=False,
            user_id="test_user_deletion"
        )

        session.add(test_todo)
        await session.commit()
        await session.refresh(test_todo)

        todo_id = test_todo.id
        assert todo_id is not None

        # Delete the todo
        await session.delete(test_todo)
        await session.commit()

    # Verify the todo was deleted
    async with AsyncSessionFactory() as session:
        statement = select(Todo).where(Todo.id == todo_id)
        result = await session.exec(statement)
        deleted_todo = result.first()

        assert deleted_todo is None


@pytest.mark.asyncio
async def test_todo_service_persistence():
    """Test that TodoService operations properly persist data."""
    async with AsyncSessionFactory() as session:
        from src.models.todo import TodoCreate, TodoUpdate

        # Create a todo via service
        todo_create = TodoCreate(
            title="Service Persistence Test",
            description="Testing service persistence",
            completed=False
        )

        created_todo = await TodoService.create_todo(session, "test_user_service_persist", todo_create)
        assert created_todo.id is not None

        # Verify via direct database access
        statement = select(Todo).where(Todo.id == created_todo.id)
        result = await session.exec(statement)
        direct_access_todo = result.first()

        assert direct_access_todo is not None
        assert direct_access_todo.title == "Service Persistence Test"
        assert direct_access_todo.user_id == "test_user_service_persist"

        # Update via service
        todo_update = TodoUpdate(
            title="Updated via Service",
            completed=True
        )

        updated_todo = await TodoService.update_todo(
            session, "test_user_service_persist", created_todo.id, todo_update
        )
        assert updated_todo is not None
        assert updated_todo.title == "Updated via Service"
        assert updated_todo.completed is True

        # Delete via service
        delete_result = await TodoService.delete_todo(
            session, "test_user_service_persist", created_todo.id
        )
        assert delete_result is True

        # Verify deletion via direct database access
        statement = select(Todo).where(Todo.id == created_todo.id)
        result = await session.exec(statement)
        post_deletion_todo = result.first()

        assert post_deletion_todo is None