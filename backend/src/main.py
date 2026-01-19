from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.v1.router import router as v1_router
from .api.v2.user_tasks import router as v2_user_tasks_router
from .api.auth import router as auth_router
from .api.v2.errors import register_error_handlers
from .utils.database import create_db_and_tables, validate_database_connection
from .config.settings import settings
from .utils.logging import setup_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    setup_logging()  # Setup logging configuration
    logger = logging.getLogger(__name__)

    logger.info(f"Starting Todo API in {settings.environment} mode")
    if settings.debug:
        logger.debug("Debug mode is ON")

    # Validate database connection
    db_ok = await validate_database_connection()
    if not db_ok:
        logger.error("Failed to connect to database. Application may not function properly.")
    else:
        logger.info("Database connection validated successfully")
        create_db_and_tables()
        logger.info("Database tables created/validated")

    yield

    # Shutdown
    logger.info("Shutting down Todo API")


app = FastAPI(
    title="Todo API",
    description="""
    API for managing Todo items in the Evolution of Todo application.

    ## Features

    - **Authentication**: Secure user signup and login with JWT tokens
    - **Version 1**: Basic todo management (public endpoints)
    - **Version 2**: JWT-protected user-scoped todo management (secure endpoints)

    ## Authentication Features

    - User registration with email and password
    - User login with JWT token issuance
    - Protected endpoints requiring valid JWT tokens
    - User isolation ensuring data privacy

    ## Version 2 Features

    - JWT-based authentication and authorization
    - User-isolated data access
    - Full CRUD operations on user-specific tasks
    - Task completion status toggling
    - Standardized error responses
    """,
    version="1.0.0",  # Updated version
    lifespan=lifespan,
    debug=settings.debug
)

# Register error handlers
register_error_handlers(app)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.debug else [],  # Allow all in debug mode, none in production by default
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    logger = logging.getLogger(__name__)
    logger.info("Root endpoint accessed")
    return {"status": "ok", "message": "Todo API is running", "environment": settings.environment}

@app.get("/health")
def health_check():
    logger = logging.getLogger(__name__)
    logger.info("Health check endpoint accessed")
    return {"status": "healthy", "environment": settings.environment, "debug": settings.debug}

# Include API routers
app.include_router(auth_router, prefix="/api/auth", tags=["authentication"])
app.include_router(v1_router, prefix="/api/v1", tags=["todos"])
app.include_router(v2_user_tasks_router, prefix="/api/v2", tags=["user-tasks-v2"])

# Include chat router for conversational bot
try:
    from .api.v1.chat import router as chat_router
    app.include_router(chat_router, prefix="/api/{user_id}", tags=["chat"])
except ImportError as e:
    import logging
    logger = logging.getLogger(__name__)
    logger.warning(f"Chat router not found. Skipping chat API endpoints. Error: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)