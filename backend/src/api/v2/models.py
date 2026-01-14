"""
API Response Models for the Todo API V2.

This module defines standardized response models for API endpoints.
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

from ..models.todo import TodoRead


class ApiResponse(BaseModel):
    """
    Standard API response wrapper.

    Attributes:
        success: Indicates if the request was successful
        data: The response data (optional)
        message: Human-readable message about the response
        timestamp: Timestamp of the response
    """
    success: bool
    data: Optional[Any] = None
    message: Optional[str] = None
    timestamp: datetime = datetime.now()


class PagedResponse(ApiResponse):
    """
    Standard API response wrapper for paginated data.

    Attributes:
        data: List of response data items
        total: Total number of items available
        page: Current page number
        limit: Number of items per page
        has_more: Indicates if more pages are available
    """
    data: List[Any]
    total: int
    page: int
    limit: int
    has_more: bool


class ErrorResponse(BaseModel):
    """
    Standard API error response.

    Attributes:
        error_code: Standardized error code
        message: Human-readable error message
        details: Additional error details (optional)
        timestamp: Timestamp of the error
    """
    error_code: str
    message: str
    details: Optional[Dict[str, Any]] = None
    timestamp: datetime = datetime.now()


class TokenResponse(ApiResponse):
    """
    API response for token-related operations.

    Attributes:
        data: Contains access token and token type
    """
    data: Dict[str, str]


class TodoListResponse(PagedResponse):
    """
    API response for todo list operations.

    Attributes:
        data: List of TodoRead objects
    """
    data: List[TodoRead]