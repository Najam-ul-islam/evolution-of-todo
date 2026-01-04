#!/usr/bin/env python3
"""Simple test to verify the todo application functionality."""

from src.todo.models import Task
from src.todo.service import TaskService
from src.todo.exceptions import ValidationError, TaskNotFound


def test_task_creation():
    """Test basic task creation and validation."""
    print("Testing task creation...")

    # Test valid task creation
    task = Task(id=1, title="Test task", description="A test task")
    assert task.title == "Test task"
    assert task.description == "A test task"
    assert task.completed == False
    print("✓ Valid task creation works")

    # Test validation
    try:
        invalid_task = Task(id=2, title="", description="Invalid task")
        assert False, "Should have raised ValueError"
    except ValueError:
        print("✓ Title validation works")

    # Test with whitespace-only title
    try:
        invalid_task = Task(id=2, title="   ", description="Invalid task")
        assert False, "Should have raised ValueError"
    except ValueError:
        print("✓ Whitespace-only title validation works")


def test_task_service():
    """Test the task service functionality."""
    print("\nTesting task service...")

    service = TaskService()

    # Test adding a task
    task1 = service.add_task("First task", "Description for first task")
    assert task1.id == 1
    assert task1.title == "First task"
    assert task1.description == "Description for first task"
    assert task1.completed == False
    print("✓ Add task works")

    # Test adding another task
    task2 = service.add_task("Second task")
    assert task2.id == 2
    assert task2.title == "Second task"
    assert task2.description is None
    print("✓ Add task with optional description works")

    # Test getting all tasks
    all_tasks = service.get_all_tasks()
    assert len(all_tasks) == 2
    assert all_tasks[0].id == 1
    assert all_tasks[1].id == 2
    print("✓ Get all tasks works")

    # Test updating a task
    updated_task = service.update_task(1, title="Updated task", description="Updated description")
    assert updated_task.title == "Updated task"
    assert updated_task.description == "Updated description"
    print("✓ Update task works")

    # Test marking task complete
    completed_task = service.mark_task_complete(1)
    assert completed_task.completed == True
    print("✓ Mark task complete works")

    # Test marking task incomplete
    incomplete_task = service.mark_task_incomplete(1)
    assert incomplete_task.completed == False
    print("✓ Mark task incomplete works")

    # Test deleting a task
    service.delete_task(2)
    remaining_tasks = service.get_all_tasks()
    assert len(remaining_tasks) == 1
    assert remaining_tasks[0].id == 1
    print("✓ Delete task works")

    # Test error handling
    try:
        service.get_task_by_id(999)
        assert False, "Should have raised TaskNotFound"
    except TaskNotFound:
        print("✓ Task not found error handling works")

    try:
        service.update_task(999, title="Non-existent task")
        assert False, "Should have raised TaskNotFound"
    except TaskNotFound:
        print("✓ Update non-existent task error handling works")

    try:
        service.update_task(1, title="")
        assert False, "Should have raised ValidationError"
    except ValidationError:
        print("✓ Validation error handling works")


if __name__ == "__main__":
    test_task_creation()
    test_task_service()
    print("\n✓ All tests passed! The Todo Console Application is working correctly.")