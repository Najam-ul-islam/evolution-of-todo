"""
API Router for user-specific task endpoints.

This module defines the API routes for user-scoped task operations with JWT protection.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel.ext.asyncio.session import AsyncSession

from ...database.connection import get_async_session
from ...models.todo import Todo, TodoCreate, TodoRead, TodoUpdate
from ...auth import get_current_user_id
from ...auth.middleware import verify_user_match
from ...services.user_task_service import UserTaskService
from ...utils.exceptions import raise_todo_not_found, raise_user_not_authorized, raise_invalid_credentials

# Create the API router
router = APIRouter(prefix="/users/{user_id}/tasks", tags=["user_tasks"])


@router.get("", response_model=List[TodoRead])
async def get_user_tasks(
    user_id: str,
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=1000)
):
    """
    Get all tasks for a specific user.

    Args:
        user_id: The ID of the user whose tasks to retrieve
        current_user_id: The ID of the currently authenticated user
        session: Database session
        skip: Number of records to skip (for pagination)
        limit: Maximum number of records to return

    Returns:
        List of TodoRead objects representing the user's tasks
    """
    # Verify that the requested user ID matches the authenticated user ID
    await verify_user_match(user_id, current_user_id)

    tasks = await UserTaskService.get_tasks_by_user(session, user_id, skip, limit)
    return tasks


@router.post("", response_model=TodoRead, status_code=status.HTTP_201_CREATED)
async def create_user_task(
    user_id: str,
    todo_create: TodoCreate,
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Create a new task for a specific user.

    Args:
        user_id: The ID of the user for whom to create the task
        todo_create: TodoCreate object with task details
        current_user_id: The ID of the currently authenticated user
        session: Database session

    Returns:
        TodoRead object representing the created task
    """
    # Verify that the requested user ID matches the authenticated user ID
    await verify_user_match(user_id, current_user_id)

    # Create the task for the user
    todo = await UserTaskService.create_task(session, user_id, todo_create)
    return todo


@router.get("/{task_id}", response_model=TodoRead)
async def get_user_task(
    user_id: str,
    task_id: int,
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Get a specific task for a user.

    Args:
        user_id: The ID of the user requesting the task
        task_id: The ID of the task to retrieve
        current_user_id: The ID of the currently authenticated user
        session: Database session

    Returns:
        TodoRead object representing the requested task
    """
    # Verify that the requested user ID matches the authenticated user ID
    await verify_user_match(user_id, current_user_id)

    # Get the specific task for the user
    todo = await UserTaskService.get_task_by_id(session, user_id, task_id)
    return todo


@router.put("/{task_id}", response_model=TodoRead)
async def update_user_task(
    user_id: str,
    task_id: int,
    todo_update: TodoUpdate,
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Update a specific task for a user.

    Args:
        user_id: The ID of the user requesting the update
        task_id: The ID of the task to update
        todo_update: TodoUpdate object with update details
        current_user_id: The ID of the currently authenticated user
        session: Database session

    Returns:
        TodoRead object representing the updated task
    """
    # Verify that the requested user ID matches the authenticated user ID
    await verify_user_match(user_id, current_user_id)

    # Update the specific task for the user
    todo = await UserTaskService.update_task(session, user_id, task_id, todo_update)
    return todo


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_task(
    user_id: str,
    task_id: int,
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Delete a specific task for a user.

    Args:
        user_id: The ID of the user requesting the deletion
        task_id: The ID of the task to delete
        current_user_id: The ID of the currently authenticated user
        session: Database session
    """
    # Verify that the requested user ID matches the authenticated user ID
    await verify_user_match(user_id, current_user_id)

    # Delete the specific task for the user
    await UserTaskService.delete_task(session, user_id, task_id)


@router.patch("/{task_id}/complete", response_model=TodoRead)
async def toggle_task_completion(
    user_id: str,
    task_id: int,
    current_user_id: str = Depends(get_current_user_id),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Toggle the completion status of a specific task for a user.

    Args:
        user_id: The ID of the user requesting the toggle
        task_id: The ID of the task to toggle
        current_user_id: The ID of the currently authenticated user
        session: Database session

    Returns:
        TodoRead object representing the task with updated completion status
    """
    # Verify that the requested user ID matches the authenticated user ID
    await verify_user_match(user_id, current_user_id)

    # Toggle the completion status of the specific task
    todo = await UserTaskService.toggle_task_completion(session, user_id, task_id)
    return todo