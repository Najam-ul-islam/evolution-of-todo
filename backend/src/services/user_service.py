from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from uuid import uuid4
from typing import Optional

from ..models.user import User, UserCreate
from ..utils.security import hash_password, verify_password


async def create_user(user_create: UserCreate, db: AsyncSession) -> User:
    """
    Create a new user with hashed password.

    Args:
        user_create: User creation data containing email and plain password
        db: Database session

    Returns:
        User: The created user object
    """
    # Hash the password
    hashed_pwd = hash_password(user_create.password)

    # Create user object with a UUID
    user = User(
        id=str(uuid4()),
        email=user_create.email,
        password_hash=hashed_pwd
    )

    # Add to database
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user


async def authenticate_user(db: AsyncSession, email: str, password: str) -> Optional[User]:
    """
    Authenticate a user by email and password.

    Args:
        db: Database session
        email: User's email address
        password: Plain text password to verify

    Returns:
        User object if authentication is successful, None otherwise
    """
    # Find user by email
    statement = select(User).where(User.email == email)
    result = await db.exec(statement)
    user = result.first()

    # Verify user exists and password is correct
    if user and verify_password(password, user.password_hash):
        return user

    return None


async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    """
    Get a user by email address.

    Args:
        db: Database session
        email: User's email address

    Returns:
        User object if found, None otherwise
    """
    statement = select(User).where(User.email == email)
    result = await db.exec(statement)
    user = result.first()
    return user


async def get_user_by_id(db: AsyncSession, user_id: str) -> Optional[User]:
    """
    Get a user by ID.

    Args:
        db: Database session
        user_id: User's ID

    Returns:
        User object if found, None otherwise
    """
    statement = select(User).where(User.id == user_id)
    result = await db.exec(statement)
    user = result.first()
    return user


async def update_user_password(db: AsyncSession, user: User, new_password: str) -> User:
    """
    Update a user's password.

    Args:
        db: Database session
        user: User object to update
        new_password: New plain text password

    Returns:
        Updated User object
    """
    # Hash the new password
    hashed_pwd = hash_password(new_password)
    user.hashed_password = hashed_pwd

    # Update in database
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user


async def deactivate_user(db: AsyncSession, user: User) -> User:
    """
    Deactivate a user account.

    Args:
        db: Database session
        user: User object to deactivate

    Returns:
        Updated User object
    """
    user.is_active = False

    # Update in database
    db.add(user)
    await db.commit()
    await db.refresh(user)

    return user