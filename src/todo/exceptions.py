"""Custom exception classes for the Todo application."""


class ValidationError(Exception):
    """Raised when input validation fails."""
    pass


class TaskNotFound(Exception):
    """Raised when an operation references a non-existent task ID."""
    pass