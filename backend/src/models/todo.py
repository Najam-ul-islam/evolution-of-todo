from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlmodel import Field, SQLModel
import uuid


class TodoBase(SQLModel):
    title: str = Field(min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False)


class Todo(TodoBase, table=True):
    id: Optional[UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: Optional[str] = Field(default=None, max_length=255, index=True)  # Changed from UUID to string
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class TodoCreate(TodoBase):
    pass


class TodoRead(TodoBase):
    id: UUID
    user_id: Optional[str]  # Changed from UUID to string
    created_at: datetime
    updated_at: datetime


class TodoUpdate(SQLModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=255)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = None