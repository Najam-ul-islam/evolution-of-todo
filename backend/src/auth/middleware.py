"""
Authentication middleware for the Todo API.

This module provides middleware for user authentication and authorization checks.
"""
from typing import Optional
from fastapi import HTTPException, status, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from ..models.todo import Todo
from ..auth.jwt_handler import verify_token, TokenData


# Initialize security scheme for JWT token extraction
security = HTTPBearer()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> TokenData:
    """
    Dependency to extract and validate JWT token from Authorization header.

    Args:
        credentials: HTTP Authorization credentials containing the JWT token

    Returns:
        TokenData: Validated token data with user information

    Raises:
        HTTPException: If token is invalid, expired, or missing
    """
    token = credentials.credentials

    token_data = verify_token(token)
    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return token_data


async def verify_user_access_for_todo(todo: Todo, user_id: str) -> bool:
    """
    Verify that the authenticated user has access to the specified todo item.

    Args:
        todo: The Todo object to check access for
        user_id: The ID of the authenticated user

    Returns:
        bool: True if the user has access to the todo item, False otherwise

    Raises:
        HTTPException: If the user does not have access to the todo item
    """
    if todo.user_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return True


async def verify_user_match(requested_user_id: str, authenticated_user_id: str) -> bool:
    """
    Verify that the requested user ID matches the authenticated user ID.

    Args:
        requested_user_id: The user ID from the request path/params
        authenticated_user_id: The user ID from the authenticated token

    Returns:
        bool: True if the user IDs match, False otherwise

    Raises:
        HTTPException: If the user IDs do not match
    """
    if requested_user_id != authenticated_user_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found or access denied"
        )
    return True