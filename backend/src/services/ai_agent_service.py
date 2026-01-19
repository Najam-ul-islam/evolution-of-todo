import json
from typing import List, Dict, Any, Optional
from openai import AsyncOpenAI
from ..models.conversation import Message
from ..schemas.chat import ToolCallSchema
from ..config.settings import settings
import logging

logger = logging.getLogger(__name__)


class AIAgentService:
    """
    Service class for integrating with OpenAI Agents SDK.
    This service handles the communication with the OpenAI API to process natural language
    and generate responses with tool usage metadata.
    """

    def __init__(self):
        # Initialize OpenAI client
        self.client = AsyncOpenAI(api_key=settings.openai_api_key) if hasattr(settings, 'openai_api_key') and settings.openai_api_key else None
        self.tools = []  # Will store available tools that the agent can use

    def register_tool(self, tool_definition: Dict[str, Any]):
        """
        Register a tool that the AI agent can use.
        """
        self.tools.append(tool_definition)

    async def process_conversation(self, messages: List[Dict[str, str]], user_query: str) -> tuple[str, List[ToolCallSchema]]:
        """
        Process a conversation with the AI agent.

        Args:
            messages: List of previous messages in the conversation (role, content)
            user_query: The current user query to process

        Returns:
            Tuple of (response_text, list_of_tool_calls)
        """
        # Prepare the conversation history for the agent
        conversation_history = messages.copy()
        conversation_history.append({"role": "user", "content": user_query})

        try:
            if self.client:
                # Make the API call to OpenAI
                response = await self.client.chat.completions.create(
                    model="gpt-3.5-turbo",  # Could be configurable
                    messages=conversation_history,
                    tools=self.tools if self.tools else None,
                    tool_choice="auto" if self.tools else None
                )

                # Extract the response
                assistant_message = response.choices[0].message

                # Extract the response text
                response_text = assistant_message.content or ""

                # Extract tool calls if any
                tool_calls = []
                if assistant_message.tool_calls:
                    for tool_call in assistant_message.tool_calls:
                        # Parse the tool call arguments
                        try:
                            tool_args = json.loads(tool_call.function.arguments) if tool_call.function.arguments else {}
                        except json.JSONDecodeError:
                            tool_args = {}

                        tool_calls.append(ToolCallSchema(
                            tool_name=tool_call.function.name,
                            tool_input=tool_args,
                            result=None  # Will be filled when the tool is actually executed
                        ))

                return response_text, tool_calls
            else:
                # Mock response when OpenAI client is not configured
                logger.warning("OpenAI API key not configured, returning mock response")
                return f"I received your message: '{user_query}'. This is a mock response since OpenAI API is not configured.", []

        except Exception as e:
            logger.error(f"Error processing conversation with AI agent: {str(e)}")
            # Return an error response
            return f"Sorry, I encountered an error processing your request: {str(e)}", []

    async def add_todo_item(self, task: str) -> Dict[str, Any]:
        """
        Mock implementation of a tool that adds a todo item.
        In a real implementation, this would call the actual todo service.
        """
        # This is a mock implementation - in reality, this would interface with the actual todo system
        return {
            "success": True,
            "task_added": task,
            "todo_id": 123  # Mock ID
        }

    async def get_todo_list(self) -> Dict[str, Any]:
        """
        Mock implementation of a tool that gets the todo list.
        """
        # This is a mock implementation
        return {
            "success": True,
            "todos": [
                {"id": 1, "task": "Buy groceries", "completed": False},
                {"id": 2, "task": "Walk the dog", "completed": True}
            ]
        }

    async def complete_todo_item(self, todo_id: int) -> Dict[str, Any]:
        """
        Mock implementation of a tool that marks a todo item as complete.
        """
        # This is a mock implementation
        return {
            "success": True,
            "todo_id": todo_id,
            "completed": True
        }

    def get_available_tools(self) -> List[Dict[str, Any]]:
        """
        Return the list of available tools for the AI agent.
        """
        return [
            {
                "type": "function",
                "function": {
                    "name": "add_todo_item",
                    "description": "Add a new todo item to the user's list",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task": {
                                "type": "string",
                                "description": "The task to add to the todo list"
                            }
                        },
                        "required": ["task"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "get_todo_list",
                    "description": "Get the user's current todo list",
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "complete_todo_item",
                    "description": "Mark a todo item as complete",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "todo_id": {
                                "type": "integer",
                                "description": "The ID of the todo item to mark as complete"
                            }
                        },
                        "required": ["todo_id"]
                    }
                }
            }
        ]


# Global instance
ai_agent_service = AIAgentService()

# Register the available tools
for tool in ai_agent_service.get_available_tools():
    ai_agent_service.register_tool(tool)