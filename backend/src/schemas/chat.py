from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class ChatRequest(BaseModel):
    """
    Schema for chat request validation.
    """
    conversation_id: Optional[int] = None
    message: str

    class Config:
        schema_extra = {
            "example": {
                "conversation_id": 456,
                "message": "Add a task to buy groceries for tomorrow"
            }
        }


class ToolCallSchema(BaseModel):
    """
    Schema for tool call representation in response.
    """
    tool_name: str
    tool_input: dict
    result: Optional[dict] = None

    class Config:
        schema_extra = {
            "example": {
                "tool_name": "add_todo_item",
                "tool_input": {
                    "task": "buy groceries for tomorrow"
                },
                "result": {
                    "success": True,
                    "todo_id": 789
                }
            }
        }


class ChatResponse(BaseModel):
    """
    Schema for chat response.
    """
    conversation_id: int
    response: str
    tool_calls: List[ToolCallSchema]

    class Config:
        schema_extra = {
            "example": {
                "conversation_id": 456,
                "response": "I've added the task 'buy groceries for tomorrow' to your todo list.",
                "tool_calls": [
                    {
                        "tool_name": "add_todo_item",
                        "tool_input": {
                            "task": "buy groceries for tomorrow"
                        },
                        "result": {
                            "success": True,
                            "todo_id": 789
                        }
                    }
                ]
            }
        }