"""
Custom exception classes for the Todo API.

This module defines custom exceptions for various error scenarios in the API.
"""
from typing import Optional
from fastapi import HTTPException, status


class TodoException(HTTPException):
    """Base exception for todo-related errors"""
    pass


class TodoNotFoundException(TodoException):
    """Raised when a todo is not found"""
    def __init__(self, todo_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Todo with id {todo_id} not found"
        )


class TodoValidationException(TodoException):
    """Raised when todo validation fails"""
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail
        )


class BaseTodoException(Exception):
    """Base exception class for all Todo API exceptions."""

    def __init__(self, message: str, details: Optional[dict] = None):
        self.message = message
        self.details = details or {}
        super().__init__(self.message)


class UserNotAuthorizedException(BaseTodoException):
    """Raised when a user is not authorized to access a resource."""

    def __init__(self, user_id: str, resource: str, details: Optional[dict] = None):
        super().__init__(
            f"User {user_id} is not authorized to access {resource}",
            {"user_id": user_id, "resource": resource, **(details or {})}
        )


class UserNotFoundException(BaseTodoException):
    """Raised when a requested user is not found."""

    def __init__(self, user_id: str, details: Optional[dict] = None):
        super().__init__(
            f"User with id {user_id} not found",
            {"user_id": user_id, **(details or {})}
        )


class JWTValidationException(BaseTodoException):
    """Raised when JWT validation fails."""

    def __init__(self, details: Optional[dict] = None):
        super().__init__(
            "JWT token validation failed",
            {"error": "invalid_token", **(details or {})}
        )


class DatabaseConnectionException(BaseTodoException):
    """Raised when there's an issue connecting to the database."""

    def __init__(self, details: Optional[dict] = None):
        super().__init__(
            "Database connection failed",
            {"error": "connection_failed", **(details or {})}
        )


class DatabaseOperationException(BaseTodoException):
    """Raised when there's an issue performing a database operation."""

    def __init__(self, operation: str, details: Optional[dict] = None):
        super().__init__(
            f"Database operation '{operation}' failed",
            {"operation": operation, **(details or {})}
        )


# HTTP Exception helpers
def raise_todo_not_found(todo_id: int) -> HTTPException:
    """Helper to raise HTTP 404 for todo not found."""
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Todo with id {todo_id} not found"
    )


def raise_user_not_authorized(user_id: str, resource: str) -> HTTPException:
    """Helper to raise HTTP 403 for unauthorized access."""
    return HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"User {user_id} is not authorized to access {resource}"
    )


def raise_invalid_credentials() -> HTTPException:
    """Helper to raise HTTP 401 for invalid credentials."""
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )


def raise_database_connection_error() -> HTTPException:
    """Helper to raise HTTP 500 for database connection errors."""
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Database connection error"
    )


def raise_database_operation_error(operation: str) -> HTTPException:
    """Helper to raise HTTP 500 for database operation errors."""
    return HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail=f"Database operation '{operation}' failed"
    )