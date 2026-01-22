"""
Base Model for MCP Task Management Tools

This module provides a base model that other models can inherit from.
Contains common fields like created_at, updated_at.
"""

from sqlmodel import SQLModel
from typing import Optional
from datetime import datetime
from pydantic import Field


class Base(SQLModel):
    """
    Base model that other models can inherit from.
    Contains common fields like created_at, updated_at.
    """
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)