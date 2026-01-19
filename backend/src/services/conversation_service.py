from sqlmodel import select, Session
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Optional, List
from datetime import datetime
from ..models.conversation import Conversation, Message, ToolCall, RoleType
from ..schemas.conversation import MessageSchema, ToolCallSchema
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status


class ConversationService:
    """
    Service class for handling conversation persistence operations.
    """

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_conversation(self, user_id: int) -> Conversation:
        """
        Create a new conversation for a user.
        """
        conversation = Conversation(
            user_id=user_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        try:
            self.session.add(conversation)
            await self.session.commit()
            await self.session.refresh(conversation)
            return conversation
        except IntegrityError:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error creating conversation"
            )

    async def get_conversation(self, conversation_id: int, user_id: int) -> Optional[Conversation]:
        """
        Get a conversation by ID for a specific user (ensures user ownership).
        """
        statement = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        result = await self.session.exec(statement)
        return result.first()

    async def save_message(self, conversation_id: int, role: RoleType, content: str) -> Message:
        """
        Save a message to a conversation.
        """
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            created_at=datetime.utcnow()
        )

        try:
            self.session.add(message)
            await self.session.commit()
            await self.session.refresh(message)
            return message
        except IntegrityError:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error saving message"
            )

    async def load_conversation_messages(self, conversation_id: int) -> List[Message]:
        """
        Load all messages for a conversation, ordered chronologically.
        """
        statement = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at.asc())

        result = await self.session.exec(statement)
        return result.all()

    async def save_tool_call(self, message_id: int, tool_name: str, tool_input: dict, result: Optional[dict] = None) -> ToolCall:
        """
        Save tool call metadata associated with a message.
        """
        tool_call = ToolCall(
            message_id=message_id,
            tool_name=tool_name,
            tool_input=str(tool_input),  # Store as JSON string
            result=str(result) if result else None,  # Store as JSON string or None
            created_at=datetime.utcnow()
        )

        try:
            self.session.add(tool_call)
            await self.session.commit()
            await self.session.refresh(tool_call)
            return tool_call
        except IntegrityError:
            await self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Error saving tool call"
            )

    async def get_messages_with_tool_calls(self, conversation_id: int) -> List[Message]:
        """
        Load all messages with their associated tool calls for a conversation.
        """
        statement = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at.asc())

        result = await self.session.exec(statement)
        messages = result.all()

        # For each message, load its tool calls
        for message in messages:
            tool_call_statement = select(ToolCall).where(
                ToolCall.message_id == message.id
            )
            tool_call_result = await self.session.exec(tool_call_statement)
            message.tool_calls = tool_call_result.all()

        return messages