import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.models.todo import Todo


def test_create_todo(client):
    response = client.post("/api/v1/todos/", json={
        "title": "Test Todo",
        "description": "This is a test todo",
        "completed": False
    })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Todo"
    assert data["description"] == "This is a test todo"
    assert data["completed"] is False


def test_get_todos(client):
    # First create a todo
    client.post("/api/v1/todos/", json={
        "title": "Test Todo for List",
        "description": "This is a test todo for list",
        "completed": False
    })

    # Then get all todos
    response = client.get("/api/v1/todos/")
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_get_todo_by_id(client):
    # First create a todo
    create_response = client.post("/api/v1/todos/", json={
        "title": "Test Todo for ID",
        "description": "This is a test todo for ID lookup",
        "completed": False
    })
    assert create_response.status_code == 200
    todo_id = create_response.json()["id"]

    # Then get the specific todo
    response = client.get(f"/api/v1/todos/{todo_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == todo_id
    assert data["title"] == "Test Todo for ID"


def test_update_todo(client):
    # First create a todo
    create_response = client.post("/api/v1/todos/", json={
        "title": "Original Title",
        "description": "Original description",
        "completed": False
    })
    assert create_response.status_code == 200
    todo_id = create_response.json()["id"]

    # Then update the todo
    update_response = client.put(f"/api/v1/todos/{todo_id}", json={
        "title": "Updated Title",
        "description": "Updated description",
        "completed": True
    })
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["title"] == "Updated Title"
    assert data["completed"] is True


def test_delete_todo(client):
    # First create a todo
    create_response = client.post("/api/v1/todos/", json={
        "title": "Test Todo for Deletion",
        "description": "This will be deleted",
        "completed": False
    })
    assert create_response.status_code == 200
    todo_id = create_response.json()["id"]

    # Then delete the todo
    delete_response = client.delete(f"/api/v1/todos/{todo_id}")
    assert delete_response.status_code == 200

    # Verify it's gone
    get_response = client.get(f"/api/v1/todos/{todo_id}")
    assert get_response.status_code == 404