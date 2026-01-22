from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from enum import Enum


class RoleType(str, Enum):
    user = "user"
    assistant = "assistant"


class ConversationSchema(BaseModel):
    """
    Schema for conversation representation.
    """
    id: Optional[int] = None
    user_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class MessageSchema(BaseModel):
    """
    Schema for message representation.
    """
    id: Optional[int] = None
    conversation_id: int
    role: RoleType
    content: str
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class ToolCallSchema(BaseModel):
    """
    Schema for tool call representation.
    """
    id: Optional[int] = None
    message_id: int
    tool_name: str
    tool_input: dict
    result: Optional[dict] = None
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True