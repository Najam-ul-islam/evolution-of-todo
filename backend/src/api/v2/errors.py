"""
Standardized error responses for the Todo API.

This module provides centralized error handling and standardized error responses.
"""
from typing import Optional, Dict, Any
from fastapi import HTTPException, Request, status
from fastapi.responses import JSONResponse
from datetime import datetime
import logging

from ...utils.exceptions import BaseTodoException, JWTValidationException, UserNotAuthorizedException, UserNotFoundException


# Set up logging
logger = logging.getLogger(__name__)


async def handle_base_todo_exception(request: Request, exc: BaseTodoException) -> JSONResponse:
    """
    Handle BaseTodoException and its subclasses.

    Args:
        request: The incoming request
        exc: The BaseTodoException that was raised

    Returns:
        JSONResponse with standardized error format
    """
    logger.error(f"BaseTodoException: {exc.message}, Details: {exc.details}")

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error_code": "TODO_ERROR",
            "message": exc.message,
            "details": exc.details,
            "timestamp": datetime.now().isoformat()
        }
    )


async def handle_jwt_validation_exception(request: Request, exc: JWTValidationException) -> JSONResponse:
    """
    Handle JWTValidationException specifically.

    Args:
        request: The incoming request
        exc: The JWTValidationException that was raised

    Returns:
        JSONResponse with standardized error format
    """
    logger.warning(f"JWT Validation Error: {exc.message}, Details: {exc.details}")

    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "error_code": "INVALID_JWT",
            "message": exc.message,
            "details": exc.details,
            "timestamp": datetime.now().isoformat()
        },
        headers={"WWW-Authenticate": "Bearer"}
    )


async def handle_user_not_authorized_exception(request: Request, exc: UserNotAuthorizedException) -> JSONResponse:
    """
    Handle UserNotAuthorizedException specifically.

    Args:
        request: The incoming request
        exc: The UserNotAuthorizedException that was raised

    Returns:
        JSONResponse with standardized error format
    """
    logger.warning(f"Authorization Error: {exc.message}, Details: {exc.details}")

    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={
            "error_code": "UNAUTHORIZED_ACCESS",
            "message": exc.message,
            "details": exc.details,
            "timestamp": datetime.now().isoformat()
        }
    )


async def handle_user_not_found_exception(request: Request, exc: UserNotFoundException) -> JSONResponse:
    """
    Handle UserNotFoundException specifically.

    Args:
        request: The incoming request
        exc: The UserNotFoundException that was raised

    Returns:
        JSONResponse with standardized error format
    """
    logger.info(f"User Not Found: {exc.message}, Details: {exc.details}")

    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "error_code": "USER_NOT_FOUND",
            "message": exc.message,
            "details": exc.details,
            "timestamp": datetime.now().isoformat()
        }
    )


async def handle_http_exception(request: Request, exc: HTTPException) -> JSONResponse:
    """
    Handle generic HTTPException.

    Args:
        request: The incoming request
        exc: The HTTPException that was raised

    Returns:
        JSONResponse with standardized error format
    """
    logger.info(f"HTTP Exception: {exc.status_code}, Detail: {exc.detail}")

    # Define error code based on status code
    error_codes = {
        400: "BAD_REQUEST",
        401: "UNAUTHORIZED",
        403: "FORBIDDEN",
        404: "NOT_FOUND",
        422: "VALIDATION_ERROR",
        500: "INTERNAL_SERVER_ERROR"
    }

    error_code = error_codes.get(exc.status_code, f"HTTP_{exc.status_code}")

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error_code": error_code,
            "message": str(exc.detail) if exc.detail else "An error occurred",
            "details": {},
            "timestamp": datetime.now().isoformat()
        }
    )


def register_error_handlers(app):
    """
    Register error handlers with the FastAPI application.

    Args:
        app: The FastAPI application instance
    """
    app.add_exception_handler(BaseTodoException, handle_base_todo_exception)
    app.add_exception_handler(JWTValidationException, handle_jwt_validation_exception)
    app.add_exception_handler(UserNotAuthorizedException, handle_user_not_authorized_exception)
    app.add_exception_handler(UserNotFoundException, handle_user_not_found_exception)
    app.add_exception_handler(HTTPException, handle_http_exception)

    logger.info("Error handlers registered successfully")