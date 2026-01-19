from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from enum import Enum
from uuid import UUID
import uuid
from .base import Base


class RoleType(str, Enum):
    user = "user"
    assistant = "assistant"


class Conversation(Base, table=True):
    """
    Represents a chat session between a user and the AI agent, containing a sequence of messages and associated metadata.
    """
    __tablename__ = "conversations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: UUID = Field(description="Foreign key linking to the user who owns this conversation")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to messages
    messages: List["Message"] = Relationship(back_populates="conversation", sa_relationship_kwargs={"cascade": "all, delete-orphan"})


class Message(Base, table=True):
    """
    Represents an individual exchange in a conversation, including the sender (user or assistant), timestamp, and content.
    """
    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id", description="Foreign key linking to the parent conversation")
    role: RoleType = Field(sa_column_kwargs={"name": "role"})  # "user" or "assistant"
    content: str = Field(description="The actual content of the message")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to conversation
    conversation: Optional[Conversation] = Relationship(back_populates="messages")
    # Relationship to tool calls
    tool_calls: List["ToolCall"] = Relationship(back_populates="message", sa_relationship_kwargs={"cascade": "all, delete"})

    # Validation: content must not be empty
    def __init__(self, **data):
        super().__init__(**data)
        if not self.content.strip():
            raise ValueError("Content must not be empty")


class ToolCall(Base, table=True):
    """
    Represents an action performed by the AI agent during processing, including the tool name and parameters.
    """
    __tablename__ = "tool_calls"

    id: Optional[int] = Field(default=None, primary_key=True)
    message_id: int = Field(foreign_key="messages.id", description="Foreign key linking to the message that triggered this tool call")
    tool_name: str = Field(description="Name of the tool that was called")
    tool_input: str = Field(description="Parameters passed to the tool (JSON string)")  # JSON as string
    result: Optional[str] = Field(default=None, description="Result returned by the tool (JSON string, nullable)")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to message
    message: Optional[Message] = Relationship(back_populates="tool_calls")

    # Validation: tool_name must not be empty
    def __init__(self, **data):
        super().__init__(**data)
        if not self.tool_name.strip():
            raise ValueError("Tool name must not be empty")