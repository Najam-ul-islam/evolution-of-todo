from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import cast
import logging
from ...database.connection import get_async_session
from ...schemas.chat import ChatRequest, ChatResponse
from ...services.conversation_service import ConversationService
from ...services.ai_agent_service import ai_agent_service
from ...models.conversation import RoleType
from ...services.auth_service import get_current_user_from_token
from ...models.conversation import Conversation, Message

router = APIRouter(tags=["chat"])

logger = logging.getLogger(__name__)


@router.post("/", response_model=ChatResponse)
async def chat_endpoint(
    user_id: str,  # Accept UUID as string
    chat_request: ChatRequest,
    current_user_id: str = Depends(get_current_user_from_token),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Process a chat message in a conversation.
    Handles natural language messages from users and returns AI-generated responses with tool usage metadata.
    """
    # Verify that the user_id in the path matches the authenticated user
    if str(user_id) != str(current_user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: user ID mismatch"
        )

    # Initialize conversation service
    conversation_service = ConversationService(db)

    # Resolve conversation context
    conversation: Conversation
    if chat_request.conversation_id is None:
        # Create new conversation
        conversation = await conversation_service.create_conversation(user_id=current_user_id)
        conversation_id = conversation.id
    else:
        # Load existing conversation
        conversation = await conversation_service.get_conversation(
            conversation_id=chat_request.conversation_id,
            user_id=current_user_id
        )

        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found or access denied"
            )

        conversation_id = conversation.id

    # Validate the message is not empty
    if not chat_request.message.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Message cannot be empty"
        )

    # Save user message to database
    user_message = await conversation_service.save_message(
        conversation_id=conversation_id,
        role=RoleType.user,
        content=chat_request.message
    )

    # Load full conversation history for AI agent
    conversation_history = await conversation_service.load_conversation_messages(conversation_id)

    # Format messages for AI agent consumption
    formatted_messages = []
    for msg in conversation_history:
        formatted_messages.append({
            "role": msg.role.value,
            "content": msg.content
        })

    # Process with AI agent
    try:
        response_text, tool_calls = await ai_agent_service.process_conversation(
            messages=formatted_messages,
            user_query=chat_request.message
        )
    except Exception as e:
        logger.error(f"Error processing conversation with AI agent: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing your request with AI agent"
        )

    # Save assistant response to database
    assistant_message = await conversation_service.save_message(
        conversation_id=conversation_id,
        role=RoleType.assistant,
        content=response_text
    )

    # Save tool call metadata if any
    for tool_call in tool_calls:
        await conversation_service.save_tool_call(
            message_id=assistant_message.id,
            tool_name=tool_call.tool_name,
            tool_input=tool_call.tool_input,
            result=tool_call.result
        )

    # Return the response
    return ChatResponse(
        conversation_id=conversation_id,
        response=response_text,
        tool_calls=tool_calls
    )