"""
API tests for user-specific task endpoints.

This module provides comprehensive tests for all user-task API endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from src.main import app
from src.models.todo import Todo, TodoCreate
from src.database.connection import sync_engine as engine


@pytest.fixture
def client():
    """Create a test client for the API."""
    with TestClient(app) as c:
        yield c


@pytest.fixture
def db_session():
    """Create a database session for testing."""
    with Session(engine) as session:
        yield session


def test_get_user_tasks_empty(client, valid_user_token):
    """Test getting tasks for a user with no tasks."""
    headers = {"Authorization": f"Bearer {valid_user_token}"}

    response = client.get("/api/v2/users/test_user_123/tasks", headers=headers)

    assert response.status_code == 200
    assert response.json() == []


def test_create_user_task(client, valid_user_token):
    """Test creating a task for a user."""
    headers = {"Authorization": f"Bearer {valid_user_token}"}

    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "completed": False
    }

    response = client.post(
        "/api/v2/users/test_user_123/tasks",
        json=task_data,
        headers=headers
    )

    assert response.status_code == 201
    created_task = response.json()
    assert created_task["title"] == "Test Task"
    assert created_task["description"] == "Test Description"
    assert created_task["completed"] is False
    assert created_task["user_id"] == "test_user_123"


def test_get_specific_user_task(client, valid_user_token):
    """Test getting a specific task for a user."""
    headers = {"Authorization": f"Bearer {valid_user_token}"}

    # First create a task
    task_data = {"title": "Specific Task", "description": "Specific Description"}
    create_response = client.post(
        "/api/v2/users/test_user_123/tasks",
        json=task_data,
        headers=headers
    )

    assert create_response.status_code == 201
    created_task = create_response.json()
    task_id = created_task["id"]

    # Now get the specific task
    response = client.get(
        f"/api/v2/users/test_user_123/tasks/{task_id}",
        headers=headers
    )

    assert response.status_code == 200
    retrieved_task = response.json()
    assert retrieved_task["id"] == task_id
    assert retrieved_task["title"] == "Specific Task"


def test_update_user_task(client, valid_user_token):
    """Test updating a specific task for a user."""
    headers = {"Authorization": f"Bearer {valid_user_token}"}

    # First create a task
    task_data = {"title": "Original Task", "description": "Original Description"}
    create_response = client.post(
        "/api/v2/users/test_user_123/tasks",
        json=task_data,
        headers=headers
    )

    assert create_response.status_code == 201
    created_task = create_response.json()
    task_id = created_task["id"]

    # Now update the task
    update_data = {
        "title": "Updated Task",
        "description": "Updated Description",
        "completed": True
    }

    response = client.put(
        f"/api/v2/users/test_user_123/tasks/{task_id}",
        json=update_data,
        headers=headers
    )

    assert response.status_code == 200
    updated_task = response.json()
    assert updated_task["id"] == task_id
    assert updated_task["title"] == "Updated Task"
    assert updated_task["completed"] is True


def test_delete_user_task(client, valid_user_token):
    """Test deleting a specific task for a user."""
    headers = {"Authorization": f"Bearer {valid_user_token}"}

    # First create a task
    task_data = {"title": "Task to Delete", "description": "Description to Delete"}
    create_response = client.post(
        "/api/v2/users/test_user_123/tasks",
        json=task_data,
        headers=headers
    )

    assert create_response.status_code == 201
    created_task = create_response.json()
    task_id = created_task["id"]

    # Now delete the task
    response = client.delete(
        f"/api/v2/users/test_user_123/tasks/{task_id}",
        headers=headers
    )

    assert response.status_code == 204

    # Verify the task is gone
    get_response = client.get(
        f"/api/v2/users/test_user_123/tasks/{task_id}",
        headers=headers
    )

    assert get_response.status_code == 404


def test_toggle_task_completion(client, valid_user_token):
    """Test toggling the completion status of a task."""
    headers = {"Authorization": f"Bearer {valid_user_token}"}

    # First create a task
    task_data = {"title": "Toggle Task", "description": "Toggle Description", "completed": False}
    create_response = client.post(
        "/api/v2/users/test_user_123/tasks",
        json=task_data,
        headers=headers
    )

    assert create_response.status_code == 201
    created_task = create_response.json()
    task_id = created_task["id"]
    assert created_task["completed"] is False

    # Now toggle completion
    response = client.patch(
        f"/api/v2/users/test_user_123/tasks/{task_id}/complete",
        headers=headers
    )

    assert response.status_code == 200
    toggled_task = response.json()
    assert toggled_task["id"] == task_id
    assert toggled_task["completed"] is True  # Should be toggled to True

    # Toggle again to return to False
    response = client.patch(
        f"/api/v2/users/test_user_123/tasks/{task_id}/complete",
        headers=headers
    )

    assert response.status_code == 200
    toggled_again_task = response.json()
    assert toggled_again_task["id"] == task_id
    assert toggled_again_task["completed"] is False  # Should be toggled back to False


def test_user_isolation(client, valid_user_token, another_user_token):
    """Test that users can only access their own tasks."""
    # Create a task for the first user
    headers1 = {"Authorization": f"Bearer {valid_user_token}"}
    task_data = {"title": "User 1 Task", "description": "User 1 Description"}
    create_response = client.post(
        "/api/v2/users/test_user_123/tasks",
        json=task_data,
        headers=headers1
    )

    assert create_response.status_code == 201
    created_task = create_response.json()
    task_id = created_task["id"]
    assert created_task["user_id"] == "test_user_123"

    # Second user tries to access first user's task (should fail)
    headers2 = {"Authorization": f"Bearer {another_user_token}"}
    response = client.get(
        f"/api/v2/users/test_user_123/tasks/{task_id}",
        headers=headers2
    )

    # Should return 404 to avoid information leakage
    assert response.status_code == 404

    # First user should still be able to access their own task
    response = client.get(
        f"/api/v2/users/test_user_123/tasks/{task_id}",
        headers=headers1
    )

    assert response.status_code == 200
    retrieved_task = response.json()
    assert retrieved_task["id"] == task_id
    assert retrieved_task["user_id"] == "test_user_123"


def test_unauthorized_access_without_token(client):
    """Test that API endpoints require authentication."""
    # Try to access without a token
    response = client.get("/api/v2/users/test_user_123/tasks")

    assert response.status_code == 401


def test_expired_token(client, expired_token):
    """Test that expired tokens are rejected."""
    headers = {"Authorization": f"Bearer {expired_token}"}

    response = client.get("/api/v2/users/test_user_123/tasks", headers=headers)

    assert response.status_code == 401