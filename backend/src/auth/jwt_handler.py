from datetime import datetime, timedelta
from typing import Optional
import jwt
from fastapi import HTTPException, status
from pydantic import BaseModel
from ..config.settings import settings  # Import settings to get secret from environment


# JWT configuration - use secret from environment
SECRET_KEY = settings.jwt_secret
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60  # 1 hour
REFRESH_TOKEN_EXPIRE_HOURS = 24  # 24 hours


class TokenData(BaseModel):
    user_id: Optional[str] = None


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token with optional expiration.

    Args:
        data: Dictionary containing token claims
        expires_delta: Optional timedelta for custom expiration

    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()

    # Convert user_id to string if it's a UUID
    if "user_id" in to_encode and hasattr(to_encode["user_id"], '__str__'):
        to_encode["user_id"] = str(to_encode["user_id"])

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT refresh token with optional expiration.

    Args:
        data: Dictionary containing token claims
        expires_delta: Optional timedelta for custom expiration

    Returns:
        Encoded JWT refresh token string
    """
    to_encode = data.copy()

    # Convert user_id to string if it's a UUID
    if "user_id" in to_encode and hasattr(to_encode["user_id"], '__str__'):
        to_encode["user_id"] = str(to_encode["user_id"])

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(hours=REFRESH_TOKEN_EXPIRE_HOURS)

    to_encode.update({"exp": expire, "iat": datetime.utcnow(), "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> Optional[TokenData]:
    """
    Verify a JWT token and return the token data if valid.

    Args:
        token: JWT token string to verify

    Returns:
        TokenData object if valid, None if invalid
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Check if token is expired
        exp_time = datetime.utcfromtimestamp(payload.get("exp"))
        if datetime.utcnow() > exp_time:
            return None

        user_id: str = payload.get("user_id")
        if user_id is None:
            return None

        token_data = TokenData(user_id=user_id)
        return token_data
    except jwt.JWTError:
        return None


def verify_refresh_token(token: str) -> Optional[TokenData]:
    """
    Verify a JWT refresh token and return the token data if valid.

    Args:
        token: JWT refresh token string to verify

    Returns:
        TokenData object if valid, None if invalid
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        # Check if token is expired
        exp_time = datetime.utcfromtimestamp(payload.get("exp"))
        if datetime.utcnow() > exp_time:
            return None

        # Verify this is a refresh token
        token_type = payload.get("type")
        if token_type != "refresh":
            return None

        user_id: str = payload.get("user_id")
        if user_id is None:
            return None

        token_data = TokenData(user_id=user_id)
        return token_data
    except jwt.JWTError:
        return None