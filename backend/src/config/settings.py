from typing import Optional
from pydantic_settings import BaseSettings
from enum import Enum
import os


class Environment(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TEST = "test"


class Settings(BaseSettings):
    # Database configuration
    database_url: str = "postgresql+asyncpg://username:password@localhost:5432/todo_db"

    # JWT configuration
    jwt_secret: str = "your-super-secret-jwt-key-here-make-it-long-and-random"

    # Environment
    environment: Environment = Environment.DEVELOPMENT

    # Debug mode
    debug: bool = True

    # NeonDB configuration (optional)
    neon_database_url: Optional[str] = None

    class Config:
        env_file = ".env" if os.path.exists(".env") else None
        case_sensitive = True


# Create a global settings instance
settings = Settings()