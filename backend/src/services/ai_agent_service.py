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

    async def add_task(self, task: str) -> Dict[str, Any]:
        """
        Implementation of a tool that adds a task.
        This method would interface with the actual task service.
        """
        # In a real implementation, this would call the actual task service
        # For now, return a mock implementation
        return {
            "success": True,
            "task_added": task,
            "task_id": 123  # Mock ID
        }

    async def list_tasks(self) -> Dict[str, Any]:
        """
        Implementation of a tool that gets the task list.
        """
        # This would interface with the actual task service
        # For now, return a mock implementation
        return {
            "success": True,
            "tasks": [
                {"id": 1, "title": "Buy groceries", "completed": False},
                {"id": 2, "title": "Walk the dog", "completed": True}
            ]
        }

    async def complete_task(self, task_id: int) -> Dict[str, Any]:
        """
        Implementation of a tool that marks a task as complete.
        """
        # This would interface with the actual task service
        # For now, return a mock implementation
        return {
            "success": True,
            "task_id": task_id,
            "completed": True
        }

    async def delete_task(self, task_id: int) -> Dict[str, Any]:
        """
        Implementation of a tool that deletes a task.
        """
        # This would interface with the actual task service
        # For now, return a mock implementation
        return {
            "success": True,
            "task_id": task_id,
            "deleted": True
        }

    async def update_task(self, task_id: int, title: str = None, description: str = None) -> Dict[str, Any]:
        """
        Implementation of a tool that updates a task.
        """
        # This would interface with the actual task service
        # For now, return a mock implementation
        result = {
            "success": True,
            "task_id": task_id
        }
        if title:
            result["title_updated"] = title
        if description:
            result["description_updated"] = description

        return result

    def detect_ambiguous_request(self, query: str, available_tasks: list) -> bool:
        """
        Detect if a user query refers to multiple tasks ambiguously.
        For example: "Complete the grocery task" when multiple grocery tasks exist.
        """
        query_lower = query.lower()
        task_titles = [task.get('title', '').lower() for task in available_tasks if isinstance(task, dict)]

        # Count how many tasks match the query keywords
        matched_tasks = []
        for title in task_titles:
            if any(keyword in title for keyword in query_lower.split()):
                matched_tasks.append(title)

        # If multiple tasks match, the request is ambiguous
        return len(matched_tasks) > 1

    def generate_clarification_request(self, query: str, available_tasks: list) -> str:
        """
        Generate a clarification request when the user query is ambiguous.
        """
        query_lower = query.lower()
        matching_tasks = []

        for task in available_tasks:
            if isinstance(task, dict) and 'title' in task:
                task_title = task['title'].lower()
                if any(keyword in task_title for keyword in query_lower.split()):
                    matching_tasks.append(task['title'])

        if matching_tasks:
            task_list = ", ".join([f"'{task}'" for task in matching_tasks])
            return f"Which task did you mean? I found multiple matches: {task_list}. Please be more specific."
        else:
            return f"I couldn't find any tasks matching your request: '{query}'. Please check the task name."

    def get_available_tools(self) -> List[Dict[str, Any]]:
        """
        Return the list of available tools for the AI agent.
        """
        return [
            {
                "type": "function",
                "function": {
                    "name": "add_task",
                    "description": "Add a new task to the user's list",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task": {
                                "type": "string",
                                "description": "The task to add to the user's list"
                            }
                        },
                        "required": ["task"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "list_tasks",
                    "description": "Get the user's current task list",
                    "parameters": {
                        "type": "object",
                        "properties": {}
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "complete_task",
                    "description": "Mark a task as complete",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": "integer",
                                "description": "The ID of the task to mark as complete"
                            }
                        },
                        "required": ["task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "delete_task",
                    "description": "Delete a task from the user's list",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": "integer",
                                "description": "The ID of the task to delete"
                            }
                        },
                        "required": ["task_id"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "update_task",
                    "description": "Update an existing task in the user's list",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "task_id": {
                                "type": "integer",
                                "description": "The ID of the task to update"
                            },
                            "title": {
                                "type": "string",
                                "description": "The new title for the task (optional)"
                            },
                            "description": {
                                "type": "string",
                                "description": "The new description for the task (optional)"
                            }
                        },
                        "required": ["task_id"]
                    }
                }
            }
        ]


# Global instance
ai_agent_service = AIAgentService()

# Register the available tools
for tool in ai_agent_service.get_available_tools():
    ai_agent_service.register_tool(tool)