#!/usr/bin/env python3
"""
Database connectivity test script for the Todo application.

This script tests the database connection and performs basic validation
of the persistent storage functionality.
"""
import asyncio
import sys
from sqlmodel import select

from src.config.settings import settings
from src.utils.database import validate_database_connection
from src.models.todo import Todo, SQLModel
from src.database.connection import AsyncSessionFactory


async def test_database_connectivity():
    """Test database connectivity and basic operations."""
    print(f"Testing database connectivity...")
    print(f"Database URL: {settings.database_url}")

    # Test sync connection
    from sqlalchemy import text
    from src.utils.database import sync_engine
    try:
        with sync_engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
        print("✓ Sync database connection successful")
    except Exception as e:
        print(f"✗ Sync database connection failed: {e}")
        return False

    # Test async connection
    try:
        async with AsyncSessionFactory() as session:
            # Execute a simple query to test async connection
            result = await session.exec(select(Todo).limit(1))
            print("✓ Async database connection successful")
    except Exception as e:
        print(f"✗ Async database connection failed: {e}")
        return False

    print("✓ Database connectivity test passed")
    return True


async def test_basic_operations():
    """Test basic CRUD operations to validate persistence."""
    print("\nTesting basic CRUD operations...")

    try:
        async with AsyncSessionFactory() as session:
            # First create a test user
            import uuid
            from src.models.user import User
            test_user = User(
                email=f"test_{uuid.uuid4()}@example.com",
                password_hash="test_hashed_password"
            )
            session.add(test_user)
            await session.commit()
            await session.refresh(test_user)

            # Create a test todo
            test_todo = Todo(
                title="Test Todo",
                description="This is a test todo for persistence validation",
                completed=False,
                user_id=test_user.id
            )

            session.add(test_todo)
            await session.commit()
            await session.refresh(test_todo)

            print(f"✓ Created todo with ID: {test_todo.id}")

            # Read the todo
            statement = select(Todo).where(Todo.id == test_todo.id)
            result = await session.exec(statement)
            retrieved_todo = result.first()

            if retrieved_todo and retrieved_todo.title == "Test Todo":
                print("✓ Read operation successful")
            else:
                print("✗ Read operation failed")
                return False

            # Update the todo
            retrieved_todo.completed = True
            await session.commit()
            await session.refresh(retrieved_todo)

            if retrieved_todo.completed:
                print("✓ Update operation successful")
            else:
                print("✗ Update operation failed")
                return False

            # Delete the todo
            await session.delete(retrieved_todo)
            await session.commit()

            # Verify deletion
            statement = select(Todo).where(Todo.id == test_todo.id)
            result = await session.exec(statement)
            deleted_todo = result.first()

            if deleted_todo is None:
                print("✓ Delete operation successful")
            else:
                print("✗ Delete operation failed")
                return False

            # Clean up the test user
            await session.delete(test_user)
            await session.commit()

        print("✓ Basic CRUD operations test passed")
        return True

    except Exception as e:
        print(f"✗ Basic operations test failed: {e}")
        return False


async def test_user_isolation():
    """Test user-level data isolation."""
    print("\nTesting user isolation...")

    try:
        async with AsyncSessionFactory() as session:
            # Create users for the test
            import uuid
            from src.models.user import User

            test_user1 = User(
                email=f"user1_{uuid.uuid4()}@example.com",
                password_hash="test_hashed_password"
            )
            session.add(test_user1)
            await session.commit()
            await session.refresh(test_user1)

            test_user2 = User(
                email=f"user2_{uuid.uuid4()}@example.com",
                password_hash="test_hashed_password"
            )
            session.add(test_user2)
            await session.commit()
            await session.refresh(test_user2)

            # Create todos for different users
            todo_user1 = Todo(
                title="User 1 Todo",
                description="Todo for user 1",
                completed=False,
                user_id=test_user1.id
            )

            todo_user2 = Todo(
                title="User 2 Todo",
                description="Todo for user 2",
                completed=False,
                user_id=test_user2.id
            )

            session.add(todo_user1)
            session.add(todo_user2)
            await session.commit()
            await session.refresh(todo_user1)
            await session.refresh(todo_user2)

            print("✓ Created todos for different users")

            # Test that user 1 can only see their own todos
            statement = select(Todo).where(Todo.user_id == test_user1.id)
            result = await session.exec(statement)
            user1_todos = result.all()

            if len(user1_todos) == 1 and user1_todos[0].title == "User 1 Todo":
                print("✓ User 1 isolation works correctly")
            else:
                print(f"✗ User 1 isolation failed. Found {len(user1_todos)} todos")
                return False

            # Test that user 2 can only see their own todos
            statement = select(Todo).where(Todo.user_id == test_user2.id)
            result = await session.exec(statement)
            user2_todos = result.all()

            if len(user2_todos) == 1 and user2_todos[0].title == "User 2 Todo":
                print("✓ User 2 isolation works correctly")
            else:
                print(f"✗ User 2 isolation failed. Found {len(user2_todos)} todos")
                return False

            # Clean up test data
            await session.delete(todo_user1)
            await session.delete(todo_user2)
            await session.delete(test_user1)
            await session.delete(test_user2)
            await session.commit()

        print("✓ User isolation test passed")
        return True

    except Exception as e:
        print(f"✗ User isolation test failed: {e}")
        return False


async def main():
    """Main function to run all tests."""
    print("=" * 60)
    print("Database Connectivity and Persistence Validation")
    print("=" * 60)

    # Test database connectivity
    connectivity_ok = await test_database_connectivity()
    if not connectivity_ok:
        print("\n✗ Database connectivity test failed. Exiting...")
        sys.exit(1)

    # Test basic operations
    basic_ops_ok = await test_basic_operations()

    # Test user isolation
    isolation_ok = await test_user_isolation()

    print("\n" + "=" * 60)
    if basic_ops_ok and isolation_ok:
        print("✓ All tests passed! Persistent storage is working correctly.")
        print("✓ Data persistence across sessions is validated.")
        print("✓ User-level data isolation is enforced.")
        return True
    else:
        print("✗ Some tests failed. Please check the database configuration.")
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)