"""
User Task Service for the Todo API.

This module provides business logic for user-specific task operations with proper user isolation.
"""
from typing import List, Optional
from sqlmodel import Session, select
from fastapi import HTTPException, status

from ..models.todo import Todo, TodoCreate, TodoUpdate
from ..utils.exceptions import TodoNotFoundException, UserNotAuthorizedException


class UserTaskService:
    """
    Service class for handling user-specific task operations.

    This class provides methods for creating, reading, updating, and deleting tasks
    while enforcing user isolation to ensure users can only access their own tasks.
    """

    @staticmethod
    def get_tasks_by_user(session: Session, user_id: str, skip: int = 0, limit: int = 100) -> List[Todo]:
        """
        Get all tasks for a specific user.

        Args:
            session: Database session
            user_id: ID of the user whose tasks to retrieve
            skip: Number of records to skip (for pagination)
            limit: Maximum number of records to return

        Returns:
            List of Todo objects belonging to the specified user
        """
        statement = (
            select(Todo)
            .where(Todo.user_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        tasks = session.exec(statement).all()
        return tasks

    @staticmethod
    def create_task(session: Session, user_id: str, todo_create: TodoCreate) -> Todo:
        """
        Create a new task for a specific user.

        Args:
            session: Database session
            user_id: ID of the user for whom to create the task
            todo_create: TodoCreate object with task details

        Returns:
            Created Todo object
        """
        todo_data = todo_create.dict()
        todo_data['user_id'] = user_id
        todo = Todo(**todo_data)
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo

    @staticmethod
    def get_task_by_id(session: Session, user_id: str, task_id: int) -> Todo:
        """
        Get a specific task by ID for a specific user.

        Args:
            session: Database session
            user_id: ID of the user requesting the task
            task_id: ID of the task to retrieve

        Returns:
            Todo object if found and user has access

        Raises:
            HTTPException: If task not found or user not authorized
        """
        statement = select(Todo).where(Todo.id == task_id, Todo.user_id == user_id)
        todo = session.exec(statement).first()

        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        return todo

    @staticmethod
    def update_task(session: Session, user_id: str, task_id: int, todo_update: TodoUpdate) -> Todo:
        """
        Update a specific task by ID for a specific user.

        Args:
            session: Database session
            user_id: ID of the user requesting the update
            task_id: ID of the task to update
            todo_update: TodoUpdate object with update details

        Returns:
            Updated Todo object

        Raises:
            HTTPException: If task not found or user not authorized
        """
        statement = select(Todo).where(Todo.id == task_id, Todo.user_id == user_id)
        todo = session.exec(statement).first()

        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        # Update the todo with new values
        update_data = todo_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(todo, field, value)

        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo

    @staticmethod
    def delete_task(session: Session, user_id: str, task_id: int) -> bool:
        """
        Delete a specific task by ID for a specific user.

        Args:
            session: Database session
            user_id: ID of the user requesting the deletion
            task_id: ID of the task to delete

        Returns:
            True if task was deleted, False otherwise

        Raises:
            HTTPException: If task not found or user not authorized
        """
        statement = select(Todo).where(Todo.id == task_id, Todo.user_id == user_id)
        todo = session.exec(statement).first()

        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        session.delete(todo)
        session.commit()
        return True

    @staticmethod
    def toggle_task_completion(session: Session, user_id: str, task_id: int) -> Todo:
        """
        Toggle the completion status of a specific task for a specific user.

        Args:
            session: Database session
            user_id: ID of the user requesting the toggle
            task_id: ID of the task to toggle

        Returns:
            Updated Todo object with toggled completion status

        Raises:
            HTTPException: If task not found or user not authorized
        """
        statement = select(Todo).where(Todo.id == task_id, Todo.user_id == user_id)
        todo = session.exec(statement).first()

        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        # Toggle the completion status
        todo.completed = not todo.completed
        session.add(todo)
        session.commit()
        session.refresh(todo)
        return todo

    @staticmethod
    def verify_user_access_to_task(session: Session, user_id: str, task_id: int) -> bool:
        """
        Verify that a user has access to a specific task.

        Args:
            session: Database session
            user_id: ID of the user to verify access for
            task_id: ID of the task to check access to

        Returns:
            True if user has access to the task, False otherwise
        """
        statement = select(Todo).where(Todo.id == task_id, Todo.user_id == user_id)
        todo = session.exec(statement).first()
        return todo is not None

    @staticmethod
    def verify_user_exists(session: Session, user_id: str) -> bool:
        """
        Verify that a user exists (has at least one task).

        Args:
            session: Database session
            user_id: ID of the user to verify existence for

        Returns:
            True if user exists (has tasks), False otherwise
        """
        statement = select(Todo).where(Todo.user_id == user_id).limit(1)
        todo = session.exec(statement).first()
        return todo is not None