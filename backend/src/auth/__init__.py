"""
Authentication utilities and dependencies for the Todo API.

This module provides JWT-based authentication dependencies for use with FastAPI.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from .jwt_handler import verify_token, TokenData

# Initialize security scheme
security = HTTPBearer()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> TokenData:
    """
    Dependency to get the current authenticated user from the JWT token.

    Args:
        credentials: HTTP authorization credentials containing the JWT token

    Returns:
        TokenData: The validated token data containing user information

    Raises:
        HTTPException: If the token is invalid or could not be validated
    """
    token_data = verify_token(credentials.credentials)
    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token_data


async def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """
    Dependency to get the current authenticated user's ID from the JWT token.

    Args:
        credentials: HTTP authorization credentials containing the JWT token

    Returns:
        str: The authenticated user's ID

    Raises:
        HTTPException: If the token is invalid, missing user_id, or could not be validated
    """
    token_data = verify_token(credentials.credentials)
    if token_data is None or not token_data.user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials or user_id missing",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token_data.user_id