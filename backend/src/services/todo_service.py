"""
Todo Service for the Todo application.

This module provides business logic for Todo operations with proper user isolation.
"""
from typing import List, Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from ..models.todo import Todo, TodoCreate, TodoUpdate
from ..utils.exceptions import (
    TodoNotFoundException,
    DatabaseOperationException,
    UserNotAuthorizedException
)


class TodoService:
    """
    Service class for handling Todo operations with user isolation.

    This class provides methods for creating, reading, updating, and deleting
    todos while enforcing user isolation to ensure users can only access their own todos.
    """

    @staticmethod
    async def get_todos_by_user(session: AsyncSession, user_id: str, skip: int = 0, limit: int = 100) -> List[Todo]:
        """
        Get all todos for a specific user.

        Args:
            session: Database session
            user_id: ID of the user whose todos to retrieve
            skip: Number of records to skip (for pagination)
            limit: Maximum number of records to return

        Returns:
            List of Todo objects belonging to the specified user

        Raises:
            DatabaseOperationException: If there's an error accessing the database
        """
        try:
            statement = (
                select(Todo)
                .where(Todo.user_id == user_id)
                .offset(skip)
                .limit(limit)
            )
            result = await session.exec(statement)
            return result.all()
        except Exception as e:
            raise DatabaseOperationException("get_todos_by_user", {"user_id": user_id, "error": str(e)})

    @staticmethod
    async def create_todo(session: AsyncSession, user_id: str, todo_create: TodoCreate) -> Todo:
        """
        Create a new todo for a specific user.

        Args:
            session: Database session
            user_id: ID of the user for whom to create the todo
            todo_create: TodoCreate object with todo details

        Returns:
            Created Todo object

        Raises:
            DatabaseOperationException: If there's an error creating the todo
        """
        try:
            todo_data = todo_create.model_dump()
            todo_data['user_id'] = user_id
            db_todo = Todo(**todo_data)
            session.add(db_todo)
            await session.commit()
            await session.refresh(db_todo)
            return db_todo
        except Exception as e:
            raise DatabaseOperationException("create_todo", {"user_id": user_id, "error": str(e)})

    @staticmethod
    async def get_todo_by_id(session: AsyncSession, user_id: str, todo_id: int) -> Optional[Todo]:
        """
        Get a specific todo by ID for a specific user.

        Args:
            session: Database session
            user_id: ID of the user requesting the todo
            todo_id: ID of the todo to retrieve

        Returns:
            Todo object if found and user has access, None otherwise

        Raises:
            DatabaseOperationException: If there's an error retrieving the todo
        """
        try:
            statement = select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
            result = await session.exec(statement)
            return result.first()
        except Exception as e:
            raise DatabaseOperationException("get_todo_by_id", {"user_id": user_id, "todo_id": todo_id, "error": str(e)})

    @staticmethod
    async def update_todo(session: AsyncSession, user_id: str, todo_id: int, todo_update: TodoUpdate) -> Optional[Todo]:
        """
        Update a specific todo by ID for a specific user.

        Args:
            session: Database session
            user_id: ID of the user requesting the update
            todo_id: ID of the todo to update
            todo_update: TodoUpdate object with update details

        Returns:
            Updated Todo object if successful, None if not found or unauthorized

        Raises:
            DatabaseOperationException: If there's an error updating the todo
        """
        try:
            statement = select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
            result = await session.exec(statement)
            db_todo = result.first()

            if not db_todo:
                return None

            # Update the todo with new values
            update_data = todo_update.model_dump(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_todo, field, value)

            await session.commit()
            await session.refresh(db_todo)
            return db_todo
        except Exception as e:
            raise DatabaseOperationException("update_todo", {"user_id": user_id, "todo_id": todo_id, "error": str(e)})

    @staticmethod
    async def delete_todo(session: AsyncSession, user_id: str, todo_id: int) -> bool:
        """
        Delete a specific todo by ID for a specific user.

        Args:
            session: Database session
            user_id: ID of the user requesting the deletion
            todo_id: ID of the todo to delete

        Returns:
            True if todo was deleted, False if not found or unauthorized

        Raises:
            DatabaseOperationException: If there's an error deleting the todo
        """
        try:
            statement = select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
            result = await session.exec(statement)
            db_todo = result.first()

            if not db_todo:
                return False

            await session.delete(db_todo)
            await session.commit()
            return True
        except Exception as e:
            raise DatabaseOperationException("delete_todo", {"user_id": user_id, "todo_id": todo_id, "error": str(e)})

    @staticmethod
    async def toggle_completion(session: AsyncSession, user_id: str, todo_id: int) -> Optional[Todo]:
        """
        Toggle the completion status of a specific todo for a specific user.

        Args:
            session: Database session
            user_id: ID of the user requesting the toggle
            todo_id: ID of the todo to toggle

        Returns:
            Updated Todo object with toggled completion status, None if not found or unauthorized

        Raises:
            DatabaseOperationException: If there's an error toggling the completion status
        """
        try:
            statement = select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
            result = await session.exec(statement)
            db_todo = result.first()

            if not db_todo:
                return None

            # Toggle the completion status
            db_todo.completed = not db_todo.completed
            await session.commit()
            await session.refresh(db_todo)
            return db_todo
        except Exception as e:
            raise DatabaseOperationException("toggle_completion", {"user_id": user_id, "todo_id": todo_id, "error": str(e)})

    @staticmethod
    async def verify_user_access_to_todo(session: AsyncSession, user_id: str, todo_id: int) -> bool:
        """
        Verify that a user has access to a specific todo.

        Args:
            session: Database session
            user_id: ID of the user to verify access for
            todo_id: ID of the todo to check access to

        Returns:
            True if user has access to the todo, False otherwise

        Raises:
            DatabaseOperationException: If there's an error checking access
        """
        try:
            statement = select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
            result = await session.exec(statement)
            todo = result.first()
            return todo is not None
        except Exception as e:
            raise DatabaseOperationException("verify_user_access", {"user_id": user_id, "todo_id": todo_id, "error": str(e)})