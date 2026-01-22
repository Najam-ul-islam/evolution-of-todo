"""
Validation Service for MCP Task Management Tools

This module provides validation utilities for the MCP tools,
enforcing parameter validation and user ownership checks.
"""

from typing import Any, Dict, Optional
from ..tools.schemas import (
    AddTaskParams,
    ListTasksParams,
    UpdateTaskParams,
    CompleteTaskParams,
    DeleteTaskParams
)


class ValidationService:
    """
    Service class that provides validation utilities for MCP tools.
    """

    @staticmethod
    def validate_add_task_params(params: Dict[str, Any]) -> AddTaskParams:
        """
        Validate parameters for the add_task tool.

        Args:
            params: Dictionary containing user_id, title, and optional description

        Returns:
            Validated AddTaskParams object

        Raises:
            ValueError: If parameters are invalid
        """
        try:
            validated_params = AddTaskParams(**params)
            return validated_params
        except Exception as e:
            raise ValueError(f"Invalid parameters for add_task: {str(e)}")

    @staticmethod
    def validate_list_tasks_params(params: Dict[str, Any]) -> ListTasksParams:
        """
        Validate parameters for the list_tasks tool.

        Args:
            params: Dictionary containing user_id and optional status

        Returns:
            Validated ListTasksParams object

        Raises:
            ValueError: If parameters are invalid
        """
        try:
            validated_params = ListTasksParams(**params)
            return validated_params
        except Exception as e:
            raise ValueError(f"Invalid parameters for list_tasks: {str(e)}")

    @staticmethod
    def validate_update_task_params(params: Dict[str, Any]) -> UpdateTaskParams:
        """
        Validate parameters for the update_task tool.

        Args:
            params: Dictionary containing user_id, task_id, and optional fields

        Returns:
            Validated UpdateTaskParams object

        Raises:
            ValueError: If parameters are invalid
        """
        try:
            validated_params = UpdateTaskParams(**params)
            return validated_params
        except Exception as e:
            raise ValueError(f"Invalid parameters for update_task: {str(e)}")

    @staticmethod
    def validate_complete_task_params(params: Dict[str, Any]) -> CompleteTaskParams:
        """
        Validate parameters for the complete_task tool.

        Args:
            params: Dictionary containing user_id and task_id

        Returns:
            Validated CompleteTaskParams object

        Raises:
            ValueError: If parameters are invalid
        """
        try:
            validated_params = CompleteTaskParams(**params)
            return validated_params
        except Exception as e:
            raise ValueError(f"Invalid parameters for complete_task: {str(e)}")

    @staticmethod
    def validate_delete_task_params(params: Dict[str, Any]) -> DeleteTaskParams:
        """
        Validate parameters for the delete_task tool.

        Args:
            params: Dictionary containing user_id and task_id

        Returns:
            Validated DeleteTaskParams object

        Raises:
            ValueError: If parameters are invalid
        """
        try:
            validated_params = DeleteTaskParams(**params)
            return validated_params
        except Exception as e:
            raise ValueError(f"Invalid parameters for delete_task: {str(e)}")

    @staticmethod
    def validate_required_fields(params: Dict[str, Any], required_fields: list) -> bool:
        """
        Validate that all required fields are present in the parameters.

        Args:
            params: Dictionary of parameters to validate
            required_fields: List of required field names

        Returns:
            True if all required fields are present, False otherwise
        """
        for field in required_fields:
            if field not in params or params[field] is None:
                return False
        return True

    @staticmethod
    def validate_user_ownership(user_id: str, provided_user_id: str) -> bool:
        """
        Validate that the user_id matches the provided_user_id for ownership verification.

        Args:
            user_id: The authenticated user ID
            provided_user_id: The user ID provided in the request

        Returns:
            True if user IDs match, False otherwise
        """
        return user_id == provided_user_id

    @staticmethod
    def validate_task_exists(task_id: int, task_list: list) -> bool:
        """
        Validate that a task with the given ID exists in the provided task list.

        Args:
            task_id: The ID of the task to validate
            task_list: List of tasks to search in

        Returns:
            True if task exists, False otherwise
        """
        return any(task.get('id') == task_id for task in task_list)


# Global instance of the validation service
validation_service = ValidationService()