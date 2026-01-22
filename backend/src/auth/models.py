"""
User context models for the Todo API.

This module defines models related to user authentication and authorization.
"""
from pydantic import BaseModel
from typing import Optional


class UserContext(BaseModel):
    """
    Represents the context of an authenticated user.

    Attributes:
        user_id: The unique identifier of the authenticated user
        username: The username of the authenticated user (optional)
        permissions: List of permissions associated with the user (optional)
    """
    user_id: str
    username: Optional[str] = None
    permissions: list[str] = []


class UserCredentials(BaseModel):
    """
    Represents user credentials for authentication.

    Attributes:
        username: The username for authentication
        password: The password for authentication
    """
    username: str
    password: str