from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field
from enum import Enum
import os


class Environment(str, Enum):
    DEVELOPMENT = "development"
    PRODUCTION = "production"
    TEST = "test"


class Settings(BaseSettings):
    # Database configuration
    database_url: str = Field(default="", alias="DATABASE_URL")

    # JWT configuration
    jwt_secret: str = Field(default="", alias="JWT_SECRET")
    jwt_access_token_expire_minutes: int = Field(default=60, alias="JWT_ACCESS_TOKEN_EXPIRE_MINUTES")
    jwt_refresh_token_expire_hours: int = Field(default=24, alias="JWT_REFRESH_TOKEN_EXPIRE_HOURS")

    # OpenAI configuration
    openai_api_key: Optional[str] = Field(default=None, alias="OPENAI_API_KEY")

    # Environment
    environment: Environment = Field(default=Environment.DEVELOPMENT, alias="ENVIRONMENT")

    # Debug mode
    debug: bool = Field(default=False, alias="DEBUG")

    # NeonDB configuration (optional)
    neon_database_url: Optional[str] = Field(default=None, alias="NEON_DATABASE_URL")

    class Config:
        env_file = ".env" if os.path.exists(".env") else None
        case_sensitive = True
        populate_by_name = True  # Allow both field names and aliases


# Create a global settings instance
settings = Settings()