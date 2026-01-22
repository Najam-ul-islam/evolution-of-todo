from fastapi import APIRouter, Depends
from typing import List
from sqlmodel.ext.asyncio.session import AsyncSession

from ...models.todo import Todo, TodoCreate, TodoRead, TodoUpdate
from ...utils.database import get_async_session, get_todo_by_id, get_all_todos, create_todo, update_todo, delete_todo
from ...utils.exceptions import TodoNotFoundException


router = APIRouter()


@router.get("/todos", response_model=List[TodoRead])
async def read_todos(
    skip: int = 0,
    limit: int = 100,
    session: AsyncSession = Depends(get_async_session)
):
    """Get all todos with pagination"""
    todos = await get_all_todos(session, offset=skip, limit=limit)
    return todos


@router.post("/todos", response_model=TodoRead)
async def create_todo_item(
    todo: TodoCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """Create a new todo"""
    db_todo = await create_todo(session, todo)
    return db_todo


@router.get("/todos/{todo_id}", response_model=TodoRead)
async def read_todo(
    todo_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """Get a specific todo by ID"""
    db_todo = await get_todo_by_id(session, todo_id)
    if not db_todo:
        raise TodoNotFoundException(todo_id)
    return db_todo


@router.put("/todos/{todo_id}", response_model=TodoRead)
async def update_todo_item(
    todo_id: int,
    todo: TodoUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    """Update a specific todo by ID"""
    db_todo = await update_todo(session, todo_id, todo)
    if not db_todo:
        raise TodoNotFoundException(todo_id)
    return db_todo


@router.delete("/todos/{todo_id}")
async def delete_todo_item(
    todo_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """Delete a specific todo by ID"""
    success = await delete_todo(session, todo_id)
    if not success:
        raise TodoNotFoundException(todo_id)
    return {"message": "Todo deleted successfully"}