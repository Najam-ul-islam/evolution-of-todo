# RESTful API Quickstart Guide

## Overview

This guide explains how to implement JWT-protected RESTful API endpoints for Todo operations with user-specific scoping. The API enforces user authentication and ensures data isolation between users.

## Prerequisites

- Existing backend infrastructure (from 001-backend-scaffolding)
- Python 3.11+ with required dependencies
- Database with user and task tables

## Setup Instructions

### 1. Install Required Dependencies

```bash
# Add JWT authentication dependencies to your existing project
pip install python-jose[cryptography] passlib[bcrypt]
# Or if using uv:
uv add python-jose[cryptography] passlib[bcrypt]
```

### 2. Configure JWT Settings

Update your settings configuration to include JWT-related parameters:

```python
# In config/settings.py (add these attributes to your Settings class)
jwt_secret_key: str = "your-super-secret-jwt-key-here-make-it-long-and-random"
jwt_algorithm: str = "HS256"
access_token_expire_minutes: int = 30
```

### 3. Create Authentication Utilities

Create a new module for JWT handling:

```python
# backend/src/auth/jwt_handler.py
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext

from ..config.settings import settings
from ..models.user import User  # Adjust import based on your user model

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)
    return encoded_jwt

def verify_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        return payload
    except JWTError:
        return None
```

### 4. Create Authentication Dependencies

Create FastAPI dependencies for token validation:

```python
# In your API route file
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user_id: str = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user_id
```

### 5. Implement User-Scoped Endpoints

Create the API endpoints with user-specific scoping:

```python
# In backend/src/api/v2/user_tasks.py
from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlmodel.ext.asyncio.session import AsyncSession

from ...models.todo import Todo, TodoCreate, TodoRead, TodoUpdate
from ...utils.database import get_async_session
from ...services.user_task_service import (
    get_user_tasks,
    create_user_task,
    get_user_task_by_id,
    update_user_task,
    delete_user_task,
    toggle_user_task_completion
)
from ..dependencies import get_current_user  # Adjust import path as needed

router = APIRouter(prefix="/api/v2", tags=["user-tasks"])

@router.get("/users/{user_id}/tasks", response_model=List[TodoRead])
async def read_user_tasks(
    user_id: str,
    current_user: str = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_async_session)
):
    if current_user != user_id:
        raise HTTPException(status_code=404, detail="Tasks not found")

    tasks = await get_user_tasks(session, user_id, skip=skip, limit=limit)
    return tasks

@router.post("/users/{user_id}/tasks", response_model=TodoRead)
async def create_user_task_endpoint(
    user_id: str,
    todo: TodoCreate,
    current_user: str = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session)
):
    if current_user != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to create tasks for this user")

    task = await create_user_task(session, user_id, todo)
    return task

# Additional endpoints would follow the same pattern...
```

## Testing the API

### 1. Authentication Flow

```bash
# Obtain a JWT token (this would typically happen during login)
curl -X POST "http://localhost:8000/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=testpass"
```

### 2. Access User-Specific Resources

```bash
# Use the obtained token to access user-specific tasks
curl -X GET "http://localhost:8000/api/v2/users/123/tasks" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN_HERE"
```

## Error Handling

The API returns appropriate HTTP status codes:

- `200 OK`: Successful requests
- `201 Created`: Successful resource creation
- `204 No Content`: Successful deletion
- `400 Bad Request`: Malformed request or validation error
- `401 Unauthorized`: Invalid or missing JWT token
- `403 Forbidden`: Valid token but insufficient privileges (in some cases)
- `404 Not Found`: Resource doesn't exist or belongs to another user
- `422 Unprocessable Entity`: Request validation failed
- `500 Internal Server Error`: Unexpected server error

## Security Considerations

- JWT tokens should have reasonable expiration times
- Always validate that the authenticated user matches the requested user ID
- Return 404 instead of 403 when users attempt to access other users' data (to prevent user enumeration)
- Use HTTPS in production to protect tokens in transit
- Implement proper token refresh mechanisms for long-lived applications