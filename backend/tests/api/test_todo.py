import pytest
from httpx import AsyncClient
from src.main import app
from src.models.todo import Todo


@pytest.mark.asyncio
async def test_create_todo():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/api/v1/todos/", json={
            "title": "Test Todo",
            "description": "This is a test todo",
            "completed": False
        })
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Todo"
    assert data["description"] == "This is a test todo"
    assert data["completed"] is False


@pytest.mark.asyncio
async def test_get_todos():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # First create a todo
        await ac.post("/api/v1/todos/", json={
            "title": "Test Todo for List",
            "description": "This is a test todo for list",
            "completed": False
        })

        # Then get all todos
        response = await ac.get("/api/v1/todos/")
    assert response.status_code == 200
    assert len(response.json()) >= 1


@pytest.mark.asyncio
async def test_get_todo_by_id():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # First create a todo
        create_response = await ac.post("/api/v1/todos/", json={
            "title": "Test Todo for ID",
            "description": "This is a test todo for ID lookup",
            "completed": False
        })
        assert create_response.status_code == 200
        todo_id = create_response.json()["id"]

        # Then get the specific todo
        response = await ac.get(f"/api/v1/todos/{todo_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == todo_id
    assert data["title"] == "Test Todo for ID"


@pytest.mark.asyncio
async def test_update_todo():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # First create a todo
        create_response = await ac.post("/api/v1/todos/", json={
            "title": "Original Title",
            "description": "Original description",
            "completed": False
        })
        assert create_response.status_code == 200
        todo_id = create_response.json()["id"]

        # Then update the todo
        update_response = await ac.put(f"/api/v1/todos/{todo_id}", json={
            "title": "Updated Title",
            "description": "Updated description",
            "completed": True
        })
        assert update_response.status_code == 200
        data = update_response.json()
        assert data["title"] == "Updated Title"
        assert data["completed"] is True


@pytest.mark.asyncio
async def test_delete_todo():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # First create a todo
        create_response = await ac.post("/api/v1/todos/", json={
            "title": "Test Todo for Deletion",
            "description": "This will be deleted",
            "completed": False
        })
        assert create_response.status_code == 200
        todo_id = create_response.json()["id"]

        # Then delete the todo
        delete_response = await ac.delete(f"/api/v1/todos/{todo_id}")
        assert delete_response.status_code == 200

        # Verify it's gone
        get_response = await ac.get(f"/api/v1/todos/{todo_id}")
        assert get_response.status_code == 404