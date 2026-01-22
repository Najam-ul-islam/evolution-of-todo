"""
Task Service Adapter for MCP Task Management Tools

This module provides an adapter layer that interfaces with the existing
backend task services while enforcing the MCP-specific contracts and constraints.
"""

import sys
import os
from typing import Any, Dict, List, Optional
from datetime import datetime

# Add the backend src directory to the Python path to access existing services
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../backend/src"))

from backend.src.database.connection import get_async_session
from backend.src.models.todo import Todo
from backend.src.models.user import User
from sqlalchemy import select
from sqlmodel.ext.asyncio.session import AsyncSession


class TaskServiceAdapter:
    """
    Adapter class that interfaces with the existing backend task services
    while enforcing MCP-specific contracts and constraints.
    """

    def __init__(self):
        """Initialize the task service adapter."""
        pass

    async def create_task(self, user_id: str, title: str, description: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a new task for a user.

        Args:
            user_id: The ID of the user creating the task
            title: The title of the task
            description: Optional description of the task

        Returns:
            Dictionary containing task_id, status, and title
        """
        async with get_async_session() as session:
            # Create a new todo item using the existing structure
            new_todo = Todo(
                user_id=user_id,
                title=title,
                description=description,
                status="pending"  # Default to pending status
            )

            session.add(new_todo)
            await session.commit()
            await session.refresh(new_todo)

            return {
                "task_id": new_todo.id,
                "status": new_todo.status,
                "title": new_todo.title
            }

    async def get_tasks(self, user_id: str, status_filter: Optional[str] = "all") -> List[Dict[str, Any]]:
        """
        Get tasks for a user with optional status filtering.

        Args:
            user_id: The ID of the user whose tasks to retrieve
            status_filter: Optional filter for task status ("all", "pending", "completed")

        Returns:
            List of task dictionaries
        """
        async with get_async_session() as session:
            # Query for todos belonging to the user
            query = select(Todo).where(Todo.user_id == user_id)

            if status_filter != "all":
                query = query.where(Todo.status == status_filter)

            result = await session.execute(query)
            todos = result.scalars().all()

            # Format the tasks as expected
            tasks = []
            for todo in todos:
                task = {
                    "id": todo.id,
                    "title": todo.title,
                    "description": todo.description or "",
                    "status": todo.status,
                    "created_at": todo.created_at.isoformat() if todo.created_at else None,
                    "updated_at": todo.updated_at.isoformat() if todo.updated_at else None
                }
                tasks.append(task)

            return tasks

    async def update_task(self, user_id: str, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Update an existing task.

        Args:
            user_id: The ID of the user who owns the task
            task_id: The ID of the task to update
            title: Optional new title for the task
            description: Optional new description for the task

        Returns:
            Dictionary containing task_id, status, and title if successful, None otherwise
        """
        async with get_async_session() as session:
            # First, check if the task belongs to the user
            query = select(Todo).where(Todo.id == task_id, Todo.user_id == user_id)
            result = await session.execute(query)
            todo = result.scalar_one_or_none()

            if not todo:
                return None

            # Update the task fields if provided
            if title is not None:
                todo.title = title
            if description is not None:
                todo.description = description

            todo.updated_at = datetime.utcnow()

            await session.commit()
            await session.refresh(todo)

            return {
                "task_id": todo.id,
                "status": todo.status,
                "title": todo.title
            }

    async def complete_task(self, user_id: str, task_id: int) -> Optional[Dict[str, Any]]:
        """
        Mark a task as completed.

        Args:
            user_id: The ID of the user who owns the task
            task_id: The ID of the task to complete

        Returns:
            Dictionary containing task_id, status, and title if successful, None otherwise
        """
        async with get_async_session() as session:
            # First, check if the task belongs to the user
            query = select(Todo).where(Todo.id == task_id, Todo.user_id == user_id)
            result = await session.execute(query)
            todo = result.scalar_one_or_none()

            if not todo:
                return None

            # Update the task status to completed
            todo.status = "completed"
            todo.updated_at = datetime.utcnow()

            await session.commit()
            await session.refresh(todo)

            return {
                "task_id": todo.id,
                "status": todo.status,
                "title": todo.title
            }

    async def delete_task(self, user_id: str, task_id: int) -> Optional[Dict[str, Any]]:
        """
        Delete a task.

        Args:
            user_id: The ID of the user who owns the task
            task_id: The ID of the task to delete

        Returns:
            Dictionary containing task_id, status, and title of the deleted task if successful, None otherwise
        """
        async with get_async_session() as session:
            # First, check if the task belongs to the user
            query = select(Todo).where(Todo.id == task_id, Todo.user_id == user_id)
            result = await session.execute(query)
            todo = result.scalar_one_or_none()

            if not todo:
                return None

            # Store the task details before deletion for the response
            task_details = {
                "task_id": todo.id,
                "status": todo.status,
                "title": todo.title
            }

            # Delete the task
            await session.delete(todo)
            await session.commit()

            # Return the task details as they existed before deletion
            return task_details

    async def verify_user_ownership(self, user_id: str, task_id: int) -> bool:
        """
        Verify that a user owns a specific task.

        Args:
            user_id: The ID of the user
            task_id: The ID of the task to verify ownership for

        Returns:
            True if the user owns the task, False otherwise
        """
        async with get_async_session() as session:
            query = select(Todo).where(Todo.id == task_id, Todo.user_id == user_id)
            result = await session.execute(query)
            todo = result.scalar_one_or_none()

            return todo is not None


# Global instance of the task service adapter
task_service = TaskServiceAdapter()