from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import Dict

from ..models.user import User, UserCreate, UserLogin
from ..utils.security import hash_password, verify_password, validate_password_strength
from ..auth.jwt_handler import create_access_token, create_refresh_token, Token
from ..database.connection import get_async_session
from ..auth.middleware import get_current_user
from ..services.user_service import create_user, authenticate_user


router = APIRouter(tags=["Authentication"])


@router.post("/register", response_model=User)
async def register(user_create: UserCreate, db: AsyncSession = Depends(get_async_session)):
    """
    Register a new user with email and password.

    Args:
        user_create: User creation data containing email and password
        db: Database session dependency

    Returns:
        User: Created user object without password

    Raises:
        HTTPException: If email already exists or password is weak
    """
    # Validate password strength
    is_valid, error_msg = validate_password_strength(user_create.password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_msg
        )

    # Check if user already exists
    existing_user = await db.exec(select(User).where(User.email == user_create.email))
    existing_user = existing_user.first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    # Create the user
    user = await create_user(user_create, db)
    return user


@router.post("/login", response_model=Token)
async def login(user_login: UserLogin, db: AsyncSession = Depends(get_async_session)):
    """
    Authenticate user with email and password, returning JWT tokens.

    Args:
        user_login: User login data containing email and password
        db: Database session dependency

    Returns:
        Token: JWT access and refresh tokens

    Raises:
        HTTPException: If credentials are invalid
    """
    user = await authenticate_user(db, user_login.email, user_login.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create JWT tokens with user_id claim
    access_token_data = {"user_id": user.id}
    refresh_token_data = {"user_id": user.id}

    access_token = create_access_token(data=access_token_data)
    refresh_token = create_refresh_token(data=refresh_token_data)

    return Token(access_token=access_token, refresh_token=refresh_token)


@router.post("/logout")
async def logout():
    """
    Invalidate user session (placeholder for future implementation).

    Returns:
        Dict: Success message
    """
    # In a JWT-only system, the client typically just discards the token
    # Server-side invalidation would require a token blacklist
    return {"message": "Successfully logged out"}


@router.get("/me", response_model=User)
async def get_current_user_from_token(
    current_user_data = Depends(get_current_user),
    db: AsyncSession = Depends(get_async_session)
):
    """
    Get current user information from the authenticated token.

    Args:
        current_user_data: The authenticated user data from token validation
        db: Database session dependency

    Returns:
        User: Current user information
    """
    # Get the full user object from the database using the user_id from the token
    result = await db.exec(select(User).where(User.id == current_user_data.user_id))
    user = result.first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return user