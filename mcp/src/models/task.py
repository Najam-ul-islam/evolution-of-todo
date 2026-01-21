"""
Task Models for MCP Task Management Tools

This module defines the data models for tasks, users, and tool calls
as specified in the feature requirements.
"""

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from enum import Enum
from .base import Base


class TaskStatus(str, Enum):
    """Enumeration of possible task statuses."""
    pending = "pending"
    completed = "completed"


class Task(Base, table=True):
    """
    Represents a user's task with properties including ID, user association,
    title, description, and status (pending/completed).
    """
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(description="Foreign key linking to the user who owns this task")
    title: str = Field(description="Title of the task")
    description: Optional[str] = Field(default=None, description="Detailed description of the task")
    status: TaskStatus = Field(default=TaskStatus.pending, description="Current status of the task")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Validation: title must not be empty
    def __init__(self, **data):
        super().__init__(**data)
        if not self.title.strip():
            raise ValueError("Title must not be empty")

        if self.status not in [TaskStatus.pending, TaskStatus.completed]:
            raise ValueError("Status must be either 'pending' or 'completed'")


class User(Base, table=True):
    """
    Represents a system user with unique identifier and associated tasks.
    """
    __tablename__ = "users"

    id: str = Field(primary_key=True, description="Unique identifier for the user")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Validation: id must be unique and not empty
    def __init__(self, **data):
        super().__init__(**data)
        if not self.id.strip():
            raise ValueError("User ID must not be empty")


class ToolCall(Base, table=True):
    """
    Represents an invocation of an MCP tool with parameters and response data.
    """
    __tablename__ = "tool_calls"

    id: Optional[int] = Field(default=None, primary_key=True)
    tool_name: str = Field(description="Name of the tool that was called")
    parameters: str = Field(description="Parameters passed to the tool (JSON string)")
    result: Optional[str] = Field(default=None, description="Result returned by the tool (JSON string)")
    user_id: str = Field(description="ID of the user who initiated the tool call")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Validation: tool_name must be one of the valid MCP tools
    def __init__(self, **data):
        super().__init__(**data)
        valid_tools = ["add_task", "list_tasks", "update_task", "complete_task", "delete_task"]

        if self.tool_name not in valid_tools:
            raise ValueError(f"Tool name must be one of {valid_tools}")

        if not self.user_id.strip():
            raise ValueError("User ID must not be empty")