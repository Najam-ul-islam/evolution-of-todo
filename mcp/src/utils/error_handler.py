"""
Error Handler Utilities for MCP Task Management Tools

This module provides standardized error responses and exception handling
for the MCP tools to ensure consistent error reporting.
"""

import json
from typing import Any, Dict, Union
from ..tools.schemas import ErrorResponse


class MCPError(Exception):
    """
    Base exception class for MCP tool errors.
    """
    def __init__(self, error_code: str, message: str):
        self.error_code = error_code
        self.message = message
        super().__init__(self.message)


class TaskNotFoundError(MCPError):
    """
    Exception raised when a task is not found.
    """
    def __init__(self, task_id: int, user_id: str):
        super().__init__(
            error_code="TASK_NOT_FOUND",
            message=f"Task with ID {task_id} not found for user {user_id}"
        )


class UnauthorizedError(MCPError):
    """
    Exception raised when unauthorized access is attempted.
    """
    def __init__(self, user_id: str, resource: str = "task"):
        super().__init__(
            error_code="UNAUTHORIZED_ACCESS",
            message=f"User {user_id} does not have access to the requested {resource}"
        )


class ValidationError(MCPError):
    """
    Exception raised when validation fails.
    """
    def __init__(self, message: str):
        super().__init__(
            error_code="VALIDATION_ERROR",
            message=message
        )


class InternalError(MCPError):
    """
    Exception raised for internal server errors.
    """
    def __init__(self, message: str = "An internal server error occurred"):
        super().__init__(
            error_code="INTERNAL_ERROR",
            message=message
        )


def handle_error(exception: Exception) -> Dict[str, str]:
    """
    Convert an exception to a standardized error response.

    Args:
        exception: The exception to handle

    Returns:
        Dictionary with error code and message
    """
    if isinstance(exception, MCPError):
        return {
            "error": exception.error_code,
            "message": exception.message
        }
    elif isinstance(exception, ValidationError):
        return {
            "error": "INVALID_PARAMETERS",
            "message": str(exception)
        }
    elif isinstance(exception, TaskNotFoundError):
        return {
            "error": "TASK_NOT_FOUND",
            "message": str(exception)
        }
    elif isinstance(exception, UnauthorizedError):
        return {
            "error": "UNAUTHORIZED_ACCESS",
            "message": str(exception)
        }
    else:
        # For any other unexpected errors, return a generic error
        return {
            "error": "INTERNAL_ERROR",
            "message": "An unexpected error occurred"
        }


def create_success_response(data: Any) -> Dict[str, Any]:
    """
    Create a standardized success response.

    Args:
        data: The data to include in the response

    Returns:
        Dictionary with success indicator and data
    """
    return {
        "success": True,
        "data": data
    }


def create_error_response(error_code: str, message: str) -> ErrorResponse:
    """
    Create a standardized error response object.

    Args:
        error_code: The error code
        message: The error message

    Returns:
        ErrorResponse object
    """
    return ErrorResponse(error=error_code, message=message)


def validate_parameters(params: Dict[str, Any], required_keys: list) -> None:
    """
    Validate that required parameters are present.

    Args:
        params: Dictionary of parameters to validate
        required_keys: List of required parameter keys

    Raises:
        ValidationError: If any required parameter is missing
    """
    for key in required_keys:
        if key not in params or params[key] is None:
            raise ValidationError(f"Missing required parameter: {key}")


def validate_user_ownership(user_id: str, requested_user_id: str) -> None:
    """
    Validate that the user has ownership of the requested resource.

    Args:
        user_id: The ID of the authenticated user
        requested_user_id: The ID of the user associated with the resource

    Raises:
        UnauthorizedError: If the user does not have ownership
    """
    if user_id != requested_user_id:
        raise UnauthorizedError(user_id)


def validate_task_exists(task_id: int, available_tasks: list) -> None:
    """
    Validate that a task exists in the available tasks list.

    Args:
        task_id: The ID of the task to validate
        available_tasks: List of available task IDs

    Raises:
        TaskNotFoundError: If the task does not exist
    """
    if task_id not in available_tasks:
        raise TaskNotFoundError(task_id, "unknown")