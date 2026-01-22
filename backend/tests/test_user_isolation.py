"""
User isolation tests for the Todo application.

This module tests that users can only access their own todos and cannot access others' data.
"""
import pytest
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from src.database.connection import AsyncSessionFactory
from src.models.todo import Todo
from src.services.todo_service import TodoService


@pytest.mark.asyncio
async def test_user_isolation_with_multiple_users():
    """Test that different users can only access their own todos."""
    async with AsyncSessionFactory() as session:
        # Create todos for multiple users
        user_a_todos = []
        user_b_todos = []

        # Create todos for User A
        for i in range(3):
            todo = Todo(
                title=f"User A Todo {i}",
                description=f"Todo {i} for User A",
                completed=False,
                user_id="user_a"
            )
            session.add(todo)
            user_a_todos.append(todo)

        # Create todos for User B
        for i in range(2):
            todo = Todo(
                title=f"User B Todo {i}",
                description=f"Todo {i} for User B",
                completed=True,
                user_id="user_b"
            )
            session.add(todo)
            user_b_todos.append(todo)

        await session.commit()

        # Refresh to get IDs
        for todo in user_a_todos + user_b_todos:
            await session.refresh(todo)

    # Verify User A can only see their own todos
    async with AsyncSessionFactory() as session:
        user_a_retrieved_todos = await TodoService.get_todos_by_user(session, "user_a")
        assert len(user_a_retrieved_todos) == 3
        for todo in user_a_retrieved_todos:
            assert todo.user_id == "user_a"
            assert todo.title.startswith("User A Todo")

    # Verify User B can only see their own todos
    async with AsyncSessionFactory() as session:
        user_b_retrieved_todos = await TodoService.get_todos_by_user(session, "user_b")
        assert len(user_b_retrieved_todos) == 2
        for todo in user_b_retrieved_todos:
            assert todo.user_id == "user_b"
            assert todo.title.startswith("User B Todo")

    # Verify User A cannot access User B's todos
    async with AsyncSessionFactory() as session:
        for b_todo in user_b_todos:
            user_a_access_to_b_todo = await TodoService.get_todo_by_id(
                session, "user_a", b_todo.id
            )
            assert user_a_access_to_b_todo is None

    # Verify User B cannot access User A's todos
    async with AsyncSessionFactory() as session:
        for a_todo in user_a_todos:
            user_b_access_to_a_todo = await TodoService.get_todo_by_id(
                session, "user_b", a_todo.id
            )
            assert user_b_access_to_a_todo is None

    # Clean up
    async with AsyncSessionFactory() as session:
        for todo in user_a_todos + user_b_todos:
            stmt = select(Todo).where(Todo.id == todo.id)
            result = await session.exec(stmt)
            todo_to_delete = result.first()
            if todo_to_delete:
                await session.delete(todo_to_delete)
        await session.commit()


@pytest.mark.asyncio
async def test_cross_user_modification_prevention():
    """Test that users cannot modify each other's todos."""
    async with AsyncSessionFactory() as session:
        from src.models.todo import TodoCreate, TodoUpdate

        # Create a todo for User A
        user_a_todo_data = TodoCreate(
            title="User A's Private Todo",
            description="This belongs to User A",
            completed=False
        )
        user_a_todo = await TodoService.create_todo(session, "user_a", user_a_todo_data)
        user_a_todo_id = user_a_todo.id

    # Try to update User A's todo as User B (should fail)
    async with AsyncSessionFactory() as session:
        update_data = TodoUpdate(
            title="Attempted Modification by User B"
        )
        update_result = await TodoService.update_todo(
            session, "user_b", user_a_todo_id, update_data
        )
        # This should return None since User B doesn't have access
        assert update_result is None

    # Verify the todo still has the original data
    async with AsyncSessionFactory() as session:
        original_todo = await TodoService.get_todo_by_id(session, "user_a", user_a_todo_id)
        assert original_todo is not None
        assert original_todo.title == "User A's Private Todo"

    # Clean up
    async with AsyncSessionFactory() as session:
        delete_result = await TodoService.delete_todo(session, "user_a", user_a_todo_id)
        assert delete_result is True


@pytest.mark.asyncio
async def test_cross_user_deletion_prevention():
    """Test that users cannot delete each other's todos."""
    async with AsyncSessionFactory() as session:
        from src.models.todo import TodoCreate

        # Create a todo for User A
        user_a_todo_data = TodoCreate(
            title="User A's Protected Todo",
            description="This should be protected from User B",
            completed=False
        )
        user_a_todo = await TodoService.create_todo(session, "user_a", user_a_todo_data)
        user_a_todo_id = user_a_todo.id

    # Try to delete User A's todo as User B (should fail)
    async with AsyncSessionFactory() as session:
        delete_result = await TodoService.delete_todo(session, "user_b", user_a_todo_id)
        # This should return False since User B doesn't have access
        assert delete_result is False

    # Verify the todo still exists
    async with AsyncSessionFactory() as session:
        original_todo = await TodoService.get_todo_by_id(session, "user_a", user_a_todo_id)
        assert original_todo is not None
        assert original_todo.title == "User A's Protected Todo"

    # User A should be able to delete their own todo
    async with AsyncSessionFactory() as session:
        delete_result = await TodoService.delete_todo(session, "user_a", user_a_todo_id)
        assert delete_result is True

        # Verify it's actually deleted
        deleted_todo = await TodoService.get_todo_by_id(session, "user_a", user_a_todo_id)
        assert deleted_todo is None


@pytest.mark.asyncio
async def test_cross_user_completion_toggle_prevention():
    """Test that users cannot toggle completion of each other's todos."""
    async with AsyncSessionFactory() as session:
        from src.models.todo import TodoCreate

        # Create a todo for User A
        user_a_todo_data = TodoCreate(
            title="User A's Toggle-Protected Todo",
            description="Completion status should be protected",
            completed=False
        )
        user_a_todo = await TodoService.create_todo(session, "user_a", user_a_todo_data)
        user_a_todo_id = user_a_todo.id

    # Try to toggle User A's todo completion as User B (should fail)
    async with AsyncSessionFactory() as session:
        toggle_result = await TodoService.toggle_completion(session, "user_b", user_a_todo_id)
        # This should return None since User B doesn't have access
        assert toggle_result is None

    # Verify the todo's completion status is unchanged
    async with AsyncSessionFactory() as session:
        original_todo = await TodoService.get_todo_by_id(session, "user_a", user_a_todo_id)
        assert original_todo is not None
        assert original_todo.completed is False

    # User A should be able to toggle their own todo
    async with AsyncSessionFactory() as session:
        toggle_result = await TodoService.toggle_completion(session, "user_a", user_a_todo_id)
        assert toggle_result is not None
        assert toggle_result.completed is True  # Should be toggled to True

        # Toggle again to return to original state
        toggle_result = await TodoService.toggle_completion(session, "user_a", user_a_todo_id)
        assert toggle_result is not None
        assert toggle_result.completed is False  # Should be toggled back to False

    # Clean up
    async with AsyncSessionFactory() as session:
        delete_result = await TodoService.delete_todo(session, "user_a", user_a_todo_id)
        assert delete_result is True


@pytest.mark.asyncio
async def test_user_isolation_with_many_users():
    """Test user isolation with a larger number of users."""
    user_ids = [f"user_{i}" for i in range(5)]
    todo_ids_by_user = {}

    # Create todos for multiple users
    async with AsyncSessionFactory() as session:
        from src.models.todo import TodoCreate

        for user_id in user_ids:
            todo_ids_by_user[user_id] = []
            for j in range(2):  # 2 todos per user
                todo_data = TodoCreate(
                    title=f"{user_id}'s Todo {j}",
                    description=f"Todo {j} for {user_id}",
                    completed=j % 2 == 0  # Alternate completion status
                )
                created_todo = await TodoService.create_todo(session, user_id, todo_data)
                todo_ids_by_user[user_id].append(created_todo.id)

    # Verify each user can only access their own todos
    for user_id in user_ids:
        async with AsyncSessionFactory() as session:
            user_todos = await TodoService.get_todos_by_user(session, user_id)
            assert len(user_todos) == 2
            for todo in user_todos:
                assert todo.user_id == user_id
                assert todo.title.startswith(f"{user_id}'s Todo")

    # Verify cross-user access prevention
    for user_id in user_ids:
        for other_user_id in user_ids:
            if user_id != other_user_id:
                for other_todo_id in todo_ids_by_user[other_user_id]:
                    async with AsyncSessionFactory() as session:
                        cross_access = await TodoService.get_todo_by_id(
                            session, user_id, other_todo_id
                        )
                        assert cross_access is None

    # Clean up
    for user_id in user_ids:
        async with AsyncSessionFactory() as session:
            for todo_id in todo_ids_by_user[user_id]:
                delete_result = await TodoService.delete_todo(session, user_id, todo_id)
                assert delete_result is True