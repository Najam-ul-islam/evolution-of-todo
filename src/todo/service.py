"""Task management service for the Todo application."""

from typing import List, Optional
from .models import Task
from .exceptions import TaskNotFound, ValidationError


class TaskService:
    """Handles business logic for task operations."""

    def __init__(self):
        """Initialize the task service with an empty task list and next ID counter."""
        self._tasks: List[Task] = []
        self._next_id: int = 1

    def add_task(self, title: str, description: Optional[str] = None) -> Task:
        """Add a new task with the given title and optional description.

        Args:
            title: The required title of the task
            description: An optional description of the task

        Returns:
            The created Task object with assigned ID and pending status

        Raises:
            ValidationError: If the title is empty or whitespace-only
        """
        if not title or not title.strip():
            raise ValidationError("Task title cannot be empty or whitespace-only")

        task = Task(
            id=self._next_id,
            title=title.strip(),
            description=description,
            completed=False
        )
        self._tasks.append(task)
        self._next_id += 1
        return task

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks.

        Returns:
            List of all Task objects
        """
        return self._tasks.copy()

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Task:
        """Update an existing task's title and/or description.

        Args:
            task_id: The ID of the task to update
            title: New title (optional)
            description: New description (optional)

        Returns:
            The updated Task object

        Raises:
            TaskNotFound: If the task with the given ID doesn't exist
        """
        task = self._find_task_by_id(task_id)

        if title is not None:
            if not title or not title.strip():
                raise ValidationError("Task title cannot be empty or whitespace-only")
            task.title = title.strip()

        if description is not None:
            task.description = description

        return task

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by its ID.

        Args:
            task_id: The ID of the task to delete

        Returns:
            True if the task was found and deleted, False otherwise

        Raises:
            TaskNotFound: If the task with the given ID doesn't exist
        """
        task = self._find_task_by_id(task_id)
        self._tasks.remove(task)
        return True

    def mark_task_complete(self, task_id: int) -> Task:
        """Mark a task as complete.

        Args:
            task_id: The ID of the task to mark complete

        Returns:
            The updated Task object with completed status

        Raises:
            TaskNotFound: If the task with the given ID doesn't exist
        """
        task = self._find_task_by_id(task_id)
        task.completed = True
        return task

    def mark_task_incomplete(self, task_id: int) -> Task:
        """Mark a task as incomplete.

        Args:
            task_id: The ID of the task to mark incomplete

        Returns:
            The updated Task object with pending status

        Raises:
            TaskNotFound: If the task with the given ID doesn't exist
        """
        task = self._find_task_by_id(task_id)
        task.completed = False
        return task

    def get_task_by_id(self, task_id: int) -> Task:
        """Find a task by its ID.

        Args:
            task_id: The ID of the task to find

        Returns:
            The Task object if found

        Raises:
            TaskNotFound: If the task with the given ID doesn't exist
        """
        for task in self._tasks:
            if task.id == task_id:
                return task
        raise TaskNotFound(f"Task with ID {task_id} does not exist")

    def _find_task_by_id(self, task_id: int) -> Task:
        """Find a task by its ID (internal method).

        Args:
            task_id: The ID of the task to find

        Returns:
            The Task object if found

        Raises:
            TaskNotFound: If the task with the given ID doesn't exist
        """
        return self.get_task_by_id(task_id)