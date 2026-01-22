"""
MCP Task Management Tools

This module implements the core task management tools that interact with the existing
backend services while enforcing user ownership and stateless operation.
"""

import sys
import os
from typing import Any, Dict, List, Optional
from datetime import datetime

# Add the backend src directory to the Python path to access existing services
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../backend/src"))

from backend.src.database.connection import get_async_session
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import select

# Import the database models and session management
from backend.src.models.todo import Todo
from backend.src.models.user import User

# Import our services
from ..services.task_service import task_service
from ..services.validation_service import validation_service
from ..utils.error_handler import (
    TaskNotFoundError,
    UnauthorizedError,
    ValidationError,
    handle_error
)


async def add_task_tool(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """
    Implements the add_task tool functionality.

    Parameters:
    - user_id (string, required): The ID of the user creating the task
    - title (string, required): The title of the task
    - description (string, optional): A description of the task

    Returns:
    - task_id: The ID of the created task
    - status: The status of the task (usually "pending")
    - title: The title of the task
    """
    try:
        # Validate input parameters
        validated_params = validation_service.validate_add_task_params(arguments)

        # Extract parameters
        user_id = validated_params.user_id
        title = validated_params.title
        description = validated_params.description

        # Use the task service to create the task
        result = await task_service.create_task(user_id, title, description)

        return result
    except Exception as e:
        # Handle any errors using the error handler
        error_response = handle_error(e)
        raise Exception(error_response["message"])


async def list_tasks_tool(arguments: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Implements the list_tasks tool functionality.

    Parameters:
    - user_id (string, required): The ID of the user whose tasks to list
    - status (string, optional): Filter by status ("all", "pending", "completed")

    Returns:
    - Array of task objects with id, title, description, and status
    """
    try:
        # Validate input parameters
        validated_params = validation_service.validate_list_tasks_params(arguments)

        # Extract parameters
        user_id = validated_params.user_id
        status_filter = validated_params.status.value if validated_params.status else "all"

        # Use the task service to get tasks
        tasks = await task_service.get_tasks(user_id, status_filter)

        return tasks
    except Exception as e:
        # Handle any errors using the error handler
        error_response = handle_error(e)
        raise Exception(error_response["message"])


async def update_task_tool(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """
    Implements the update_task tool functionality.

    Parameters:
    - user_id (string, required): The ID of the user who owns the task
    - task_id (integer, required): The ID of the task to update
    - title (string, optional): New title for the task
    - description (string, optional): New description for the task

    Returns:
    - task_id: The ID of the updated task
    - status: The status of the task
    - title: The title of the task
    """
    try:
        # Validate input parameters
        validated_params = validation_service.validate_update_task_params(arguments)

        # Extract parameters
        user_id = validated_params.user_id
        task_id = validated_params.task_id
        title = validated_params.title
        description = validated_params.description

        # Use the task service to update the task
        result = await task_service.update_task(user_id, task_id, title, description)

        if result is None:
            raise TaskNotFoundError(task_id, user_id)

        return result
    except Exception as e:
        # Handle any errors using the error handler
        error_response = handle_error(e)
        raise Exception(error_response["message"])


async def complete_task_tool(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """
    Implements the complete_task tool functionality.

    Parameters:
    - user_id (string, required): The ID of the user who owns the task
    - task_id (integer, required): The ID of the task to complete

    Returns:
    - task_id: The ID of the completed task
    - status: The status of the task ("completed")
    - title: The title of the task
    """
    try:
        # Validate input parameters
        validated_params = validation_service.validate_complete_task_params(arguments)

        # Extract parameters
        user_id = validated_params.user_id
        task_id = validated_params.task_id

        # Use the task service to complete the task
        result = await task_service.complete_task(user_id, task_id)

        if result is None:
            raise TaskNotFoundError(task_id, user_id)

        return result
    except Exception as e:
        # Handle any errors using the error handler
        error_response = handle_error(e)
        raise Exception(error_response["message"])


async def delete_task_tool(arguments: Dict[str, Any]) -> Dict[str, Any]:
    """
    Implements the delete_task tool functionality.

    Parameters:
    - user_id (string, required): The ID of the user who owns the task
    - task_id (integer, required): The ID of the task to delete

    Returns:
    - task_id: The ID of the deleted task
    - status: The status of the task at time of deletion
    - title: The title of the task
    """
    try:
        # Validate input parameters
        validated_params = validation_service.validate_delete_task_params(arguments)

        # Extract parameters
        user_id = validated_params.user_id
        task_id = validated_params.task_id

        # Use the task service to delete the task
        result = await task_service.delete_task(user_id, task_id)

        if result is None:
            raise TaskNotFoundError(task_id, user_id)

        return result
    except Exception as e:
        # Handle any errors using the error handler
        error_response = handle_error(e)
        raise Exception(error_response["message"])