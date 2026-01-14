"""
Integration tests for the Todo API V2 endpoints.

This module tests the end-to-end functionality of the JWT-protected user-scoped API endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from src.main import app
from src.utils.database import engine, get_session
from src.models.todo import Todo, TodoCreate
from src.auth.jwt_handler import create_access_token


@pytest.fixture(scope="module")
def client():
    """Create a test client for the API."""
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="function")
def db_session():
    """Create a database session for testing."""
    with Session(engine) as session:
        yield session


def test_api_v2_endpoints_integration(client, db_session):
    """
    Test the integration of all V2 API endpoints.

    This test verifies that the JWT-protected user-scoped endpoints work correctly
    with proper user isolation.
    """
    # Create a test user ID
    test_user_id = "test_user_123"

    # Create a JWT token for the test user
    token_data = {"sub": "testuser", "user_id": test_user_id}
    jwt_token = create_access_token(token_data)

    headers = {"Authorization": f"Bearer {jwt_token}"}

    # Test creating a task for the user
    create_response = client.post(
        f"/api/v2/users/{test_user_id}/tasks",
        json={"title": "Test Task", "description": "Test Description"},
        headers=headers
    )

    assert create_response.status_code == 201
    created_task = create_response.json()
    assert created_task["title"] == "Test Task"
    assert created_task["user_id"] == test_user_id

    task_id = created_task["id"]

    # Test getting the specific task
    get_response = client.get(
        f"/api/v2/users/{test_user_id}/tasks/{task_id}",
        headers=headers
    )

    assert get_response.status_code == 200
    retrieved_task = get_response.json()
    assert retrieved_task["id"] == task_id
    assert retrieved_task["title"] == "Test Task"

    # Test getting all user tasks
    get_all_response = client.get(
        f"/api/v2/users/{test_user_id}/tasks",
        headers=headers
    )

    assert get_all_response.status_code == 200
    tasks_list = get_all_response.json()
    assert len(tasks_list) == 1
    assert tasks_list[0]["id"] == task_id

    # Test updating the task
    update_response = client.put(
        f"/api/v2/users/{test_user_id}/tasks/{task_id}",
        json={"title": "Updated Task", "description": "Updated Description", "completed": True},
        headers=headers
    )

    assert update_response.status_code == 200
    updated_task = update_response.json()
    assert updated_task["id"] == task_id
    assert updated_task["title"] == "Updated Task"
    assert updated_task["completed"] is True

    # Test toggling completion status
    toggle_response = client.patch(
        f"/api/v2/users/{test_user_id}/tasks/{task_id}/complete",
        headers=headers
    )

    assert toggle_response.status_code == 200
    toggled_task = toggle_response.json()
    assert toggled_task["id"] == task_id
    assert toggled_task["completed"] is False  # Should be toggled back to False

    # Test deleting the task
    delete_response = client.delete(
        f"/api/v2/users/{test_user_id}/tasks/{task_id}",
        headers=headers
    )

    assert delete_response.status_code == 204

    # Verify the task was deleted
    get_deleted_response = client.get(
        f"/api/v2/users/{test_user_id}/tasks/{task_id}",
        headers=headers
    )

    assert get_deleted_response.status_code == 404


def test_user_isolation(client, db_session):
    """
    Test that users can only access their own tasks.

    This test verifies that the user isolation mechanism works correctly.
    """
    # Create two different user IDs
    user1_id = "user_1_test"
    user2_id = "user_2_test"

    # Create JWT tokens for both users
    token_data1 = {"sub": "user1", "user_id": user1_id}
    token_data2 = {"sub": "user2", "user_id": user2_id}

    jwt_token1 = create_access_token(token_data1)
    jwt_token2 = create_access_token(token_data2)

    headers1 = {"Authorization": f"Bearer {jwt_token1}"}
    headers2 = {"Authorization": f"Bearer {jwt_token2}"}

    # User 1 creates a task
    create_response = client.post(
        f"/api/v2/users/{user1_id}/tasks",
        json={"title": "User 1 Task", "description": "Task for user 1"},
        headers=headers1
    )

    assert create_response.status_code == 201
    task = create_response.json()
    task_id = task["id"]
    assert task["user_id"] == user1_id

    # User 2 tries to access User 1's task (should fail)
    get_response = client.get(
        f"/api/v2/users/{user1_id}/tasks/{task_id}",
        headers=headers2  # User 2 trying to access User 1's task
    )

    # Should return 404 to avoid information leakage (not 403)
    assert get_response.status_code == 404

    # User 1 should still be able to access their own task
    get_response = client.get(
        f"/api/v2/users/{user1_id}/tasks/{task_id}",
        headers=headers1  # User 1 accessing their own task
    )

    assert get_response.status_code == 200
    retrieved_task = get_response.json()
    assert retrieved_task["id"] == task_id
    assert retrieved_task["user_id"] == user1_id


if __name__ == "__main__":
    pytest.main([__file__])