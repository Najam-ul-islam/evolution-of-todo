"""Task model definition for the Todo application."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Task:
    """Represents a single todo item."""

    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False

    def __post_init__(self):
        """Validate the task after initialization."""
        if not self.title or not self.title.strip():
            raise ValueError("Task title cannot be empty or whitespace-only")