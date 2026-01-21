"""
MCP Server for Task Management Tools

This module implements a stateless MCP server that exposes task management operations as tools,
reusing existing backend task services while enforcing strict tool contracts,
ownership checks, and deterministic behavior.
"""

import asyncio
from typing import Any, Dict, List, Optional
from mcp.server import Server
from mcp.types import Tool, TextContent, Prompt
import json
from .tools.task_tools import (
    add_task_tool,
    list_tasks_tool,
    update_task_tool,
    complete_task_tool,
    delete_task_tool
)


# Create MCP server instance
server = Server("mcp-task-management-server")


@server.after_connect
async def init_tools(context) -> None:
    """Initialize all MCP tools after connection."""
    # Register all task management tools
    await context.tools.set(
        [
            Tool(
                name="add_task",
                description="Creates a new task for a user",
                input_schema={
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "ID of the user creating the task"},
                        "title": {"type": "string", "description": "Title of the task"},
                        "description": {"type": "string", "description": "Detailed description of the task (optional)"}
                    },
                    "required": ["user_id", "title"]
                }
            ),
            Tool(
                name="list_tasks",
                description="Lists tasks for a user",
                input_schema={
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "ID of the user whose tasks to list"},
                        "status": {"type": "string", "enum": ["all", "pending", "completed"], "description": "Filter by status (optional)"}
                    },
                    "required": ["user_id"]
                }
            ),
            Tool(
                name="update_task",
                description="Updates properties of an existing task",
                input_schema={
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "ID of the user who owns the task"},
                        "task_id": {"type": "integer", "description": "ID of the task to update"},
                        "title": {"type": "string", "description": "New title for the task (optional)"},
                        "description": {"type": "string", "description": "New description for the task (optional)"}
                    },
                    "required": ["user_id", "task_id"]
                }
            ),
            Tool(
                name="complete_task",
                description="Marks a task as completed",
                input_schema={
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "ID of the user who owns the task"},
                        "task_id": {"type": "integer", "description": "ID of the task to complete"}
                    },
                    "required": ["user_id", "task_id"]
                }
            ),
            Tool(
                name="delete_task",
                description="Deletes a task",
                input_schema={
                    "type": "object",
                    "properties": {
                        "user_id": {"type": "string", "description": "ID of the user who owns the task"},
                        "task_id": {"type": "integer", "description": "ID of the task to delete"}
                    },
                    "required": ["user_id", "task_id"]
                }
            )
        ]
    )


@server.call_tool
async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    """Handle tool calls from the MCP client."""
    try:
        if name == "add_task":
            result = await add_task_tool(arguments)
        elif name == "list_tasks":
            result = await list_tasks_tool(arguments)
        elif name == "update_task":
            result = await update_task_tool(arguments)
        elif name == "complete_task":
            result = await complete_task_tool(arguments)
        elif name == "delete_task":
            result = await delete_task_tool(arguments)
        else:
            raise ValueError(f"Unknown tool: {name}")

        return [TextContent(type="text", text=json.dumps(result))]

    except Exception as e:
        # Return standardized error response
        error_response = {
            "error": "INTERNAL_ERROR",
            "message": str(e)
        }
        return [TextContent(type="text", text=json.dumps(error_response))]


@server.list_prompts
async def list_prompts() -> List[Prompt]:
    """List available prompts for the MCP client."""
    return [
        Prompt(
            name="task_management_help",
            description="Provides help information about task management tools"
        )
    ]


@server.get_prompt
async def get_prompt(name: str) -> Optional[Prompt]:
    """Get a specific prompt by name."""
    if name == "task_management_help":
        return Prompt(
            name="task_management_help",
            description="Provides help information about task management tools",
            messages=[
                {
                    "role": "system",
                    "content": "The task management tools allow you to create, list, update, complete, and delete tasks. Available tools:\n- add_task: Create a new task\n- list_tasks: List tasks for a user\n- update_task: Update an existing task\n- complete_task: Mark a task as completed\n- delete_task: Delete a task"
                }
            ]
        )
    return None


if __name__ == "__main__":
    # Run the server
    import uvicorn

    # The MCP server would typically be run as a separate service
    # This is just a placeholder for the actual MCP server startup
    print("MCP Task Management Server initialized")
    print("Available tools: add_task, list_tasks, update_task, complete_task, delete_task")