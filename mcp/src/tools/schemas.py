"""
Tool Parameter and Response Schemas for MCP Task Management Tools

This module defines the schemas used for validation of tool parameters
and responses in the MCP Task Management system.
"""

from pydantic import BaseModel, validator
from typing import Optional, List, Dict, Any
from enum import Enum
from datetime import datetime


class TaskStatus(str, Enum):
    """Enumeration of possible task statuses."""
    PENDING = "pending"
    COMPLETED = "completed"
    ALL = "all"


class AddTaskParams(BaseModel):
    """Schema for add_task tool parameters."""
    user_id: str
    title: str
    description: Optional[str] = None

    @validator('user_id')
    def validate_user_id(cls, v):
        if not v or not v.strip():
            raise ValueError('user_id must be a non-empty string')
        return v

    @validator('title')
    def validate_title(cls, v):
        if not v or not v.strip():
            raise ValueError('title must be a non-empty string')
        return v


class ListTasksParams(BaseModel):
    """Schema for list_tasks tool parameters."""
    user_id: str
    status: Optional[TaskStatus] = TaskStatus.ALL

    @validator('user_id')
    def validate_user_id(cls, v):
        if not v or not v.strip():
            raise ValueError('user_id must be a non-empty string')
        return v


class UpdateTaskParams(BaseModel):
    """Schema for update_task tool parameters."""
    user_id: str
    task_id: int
    title: Optional[str] = None
    description: Optional[str] = None

    @validator('user_id')
    def validate_user_id(cls, v):
        if not v or not v.strip():
            raise ValueError('user_id must be a non-empty string')
        return v

    @validator('task_id')
    def validate_task_id(cls, v):
        if v <= 0:
            raise ValueError('task_id must be a positive integer')
        return v


class CompleteTaskParams(BaseModel):
    """Schema for complete_task tool parameters."""
    user_id: str
    task_id: int

    @validator('user_id')
    def validate_user_id(cls, v):
        if not v or not v.strip():
            raise ValueError('user_id must be a non-empty string')
        return v

    @validator('task_id')
    def validate_task_id(cls, v):
        if v <= 0:
            raise ValueError('task_id must be a positive integer')
        return v


class DeleteTaskParams(BaseModel):
    """Schema for delete_task tool parameters."""
    user_id: str
    task_id: int

    @validator('user_id')
    def validate_user_id(cls, v):
        if not v or not v.strip():
            raise ValueError('user_id must be a non-empty string')
        return v

    @validator('task_id')
    def validate_task_id(cls, v):
        if v <= 0:
            raise ValueError('task_id must be a positive integer')
        return v


class TaskResponse(BaseModel):
    """Schema for task operation responses."""
    task_id: int
    status: str
    title: str


class TaskObject(BaseModel):
    """Schema for individual task objects in list response."""
    id: int
    title: str
    description: Optional[str] = None
    status: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ListTasksResponse(BaseModel):
    """Schema for list_tasks response."""
    tasks: List[TaskObject]


class ErrorResponse(BaseModel):
    """Schema for error responses."""
    error: str
    message: str