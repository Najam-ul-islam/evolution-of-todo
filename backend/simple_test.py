#!/usr/bin/env python3
"""
Simple test to verify database connectivity with NeonDB PostgreSQL
"""
import asyncio
from sqlalchemy import text
from src.utils.database import sync_engine
from src.database.connection import AsyncSessionFactory
from src.models.todo import Todo
from sqlmodel import select
import uuid

async def simple_test():
    print("Testing database connectivity...")

    # Test sync connection
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
            result = await session.exec(select(Todo).limit(1))
        print("✓ Async database connection successful")
    except Exception as e:
        print(f"✗ Async database connection failed: {e}")
        return False

    # Test creating a user
    try:
        from src.models.user import User
        async with AsyncSessionFactory() as session:
            test_user = User(
                email=f"test_{uuid.uuid4()}@example.com",
                password_hash="test_hashed_password"
            )
            session.add(test_user)
            await session.commit()
            await session.refresh(test_user)
            user_id = test_user.id
            print(f"✓ Created test user with ID: {user_id}")

            # Clean up
            await session.delete(test_user)
            await session.commit()
    except Exception as e:
        print(f"✗ User creation test failed: {e}")
        return False

    print("✓ All database tests passed!")
    return True

if __name__ == "__main__":
    success = asyncio.run(simple_test())
    if success:
        print("\nDatabase connection with NeonDB PostgreSQL is working correctly!")
    else:
        print("\nDatabase connection test failed.")