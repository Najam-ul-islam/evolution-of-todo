# Todo Backend API

This is the FastAPI backend for the Todo application in the Evolution of Todo project.

## Features

- **Authentication**: Secure user signup and login with JWT tokens
- **Version 1**: Basic todo management (public endpoints)
- **Version 2**: JWT-protected user-scoped todo management (secure endpoints)

## Prerequisites

- Python 3.11 or higher
- uv package manager (recommended) or pip

## Setup Instructions

### 1. Clone the repository
```bash
git clone <repository-url>
cd <repository-name>
```

### 2. Navigate to the backend directory
```bash
cd backend
```

### 3. Install dependencies using uv (recommended)
```bash
# Create virtual environment
uv venv

# Activate the virtual environment
source .venv/bin/activate  # Linux/Mac
# On Windows: .venv\Scripts\activate

# Install dependencies
uv sync  # Installs all dependencies from pyproject.toml including dev dependencies
# Or install in editable mode: uv pip install -e .
```

### Alternative: Install dependencies using pip
```bash
# Create virtual environment
python -m venv .venv

# Activate the virtual environment
source .venv/bin/activate  # Linux/Mac
# On Windows: .venv\Scripts\activate

# Install dependencies
pip install -e .
# Or install with dev dependencies: pip install -e ".[dev]"
```

### 4. Set up environment variables
Copy the example environment file and configure your settings:
```bash
cp .env.example .env
```

Edit the `.env` file with your specific configuration:
- `DATABASE_URL`: PostgreSQL connection string for your NeonDB instance
- `JWT_SECRET`: Secure random string for JWT token signing (at least 32 characters)
- `BETTER_AUTH_SECRET`: Secret key for authentication (shared with frontend)
- `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`: Access token expiration time (default: 60)
- `JWT_REFRESH_TOKEN_EXPIRE_HOURS`: Refresh token expiration time (default: 24)
- `ENVIRONMENT`: Set to 'development', 'production', or 'test'
- `DEBUG`: Set to True for development, False for production

### 5. Run the application
```bash
# From the backend directory
uv run python -m src.main
# Or if using pip: python -m src.main

# Alternatively, using uvicorn directly:
cd src
uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

### 6. Run tests
```bash
# From the backend directory
uv run pytest  # If using uv
# Or: python -m pytest  # If using pip directly
```

### 7. Run database migrations (when needed)
```bash
# Using alembic (after setup)
alembic upgrade head
```

## API Endpoints

Once running, the API will be available at the following endpoints:

### Authentication Endpoints
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login and receive JWT tokens
- `POST /api/auth/logout` - Logout (client-side token removal)
- `GET /api/auth/me` - Get current user info

### Version 1 (Basic Todo API)
- `GET /` - Root endpoint with status information
- `GET /health` - Health check endpoint
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation (ReDoc)
- `GET /api/v1/todos` - Get all todos
- `POST /api/v1/todos` - Create a new todo
- `GET /api/v1/todos/{id}` - Get a specific todo
- `PUT /api/v1/todos/{id}` - Update a specific todo
- `DELETE /api/v1/todos/{id}` - Delete a specific todo

### Version 2 (JWT-Protected User-Scoped Todo API)
- `GET /api/v2/users/{user_id}/tasks` - Get all tasks for a specific user (JWT required)
- `POST /api/v2/users/{user_id}/tasks` - Create a new task for a specific user (JWT required)
- `GET /api/v2/users/{user_id}/tasks/{task_id}` - Get a specific task (JWT required)
- `PUT /api/v2/users/{user_id}/tasks/{task_id}` - Update a specific task (JWT required)
- `DELETE /api/v2/users/{user_id}/tasks/{task_id}` - Delete a specific task (JWT required)
- `PATCH /api/v2/users/{user_id}/tasks/{task_id}/complete` - Toggle completion status (JWT required)

**Note**: Version 2 endpoints require a valid JWT token in the Authorization header: `Authorization: Bearer <token>`

## Authentication

The application includes a complete authentication system with:

- User registration and login via email/password
- JWT token-based authentication (access and refresh tokens)
- Secure password hashing with bcrypt
- User isolation ensuring data privacy
- Protected endpoints requiring valid JWT tokens

### JWT Configuration

- Access tokens expire after 60 minutes (configurable)
- Refresh tokens expire after 24 hours (configurable)
- Tokens are validated using HS256 algorithm
- User ID is embedded in the token for authorization checks
- Password strength validation (min 8 chars, uppercase, lowercase, digit)

## Project Structure

```
backend/
├── src/
│   ├── main.py              # Application entry point with FastAPI app
│   ├── config/              # Configuration and settings
│   │   ├── __init__.py
│   │   └── settings.py      # Pydantic settings with environment variables
│   ├── models/              # SQLModel database models
│   │   ├── __init__.py
│   │   ├── todo.py          # Todo model definitions
│   │   └── user.py          # User model for authentication
│   ├── api/                 # API route definitions
│   │   ├── __init__.py
│   │   ├── auth.py          # Authentication endpoints
│   │   └── v1/              # Version 1 API endpoints
│   │       ├── __init__.py
│   │       └── router.py    # Todo API routes
│   ├── auth/                # Authentication utilities
│   │   ├── __init__.py
│   │   ├── jwt_handler.py   # JWT creation and validation functions
│   │   └── middleware.py    # Authentication middleware
│   ├── services/            # Business logic layer
│   │   ├── __init__.py
│   │   ├── todo_service.py  # Todo operations
│   │   ├── user_task_service.py  # User-task operations
│   │   └── user_service.py  # User operations with authentication
│   └── utils/               # Utility functions
│       ├── __init__.py
│       ├── database.py      # Database utilities and session management
│       ├── logging.py       # Logging configuration
│       ├── exceptions.py    # Custom exceptions
│       └── security.py      # Security utilities (hashing, etc.)
├── alembic/                 # Database migration scripts
│   ├── env.py               # Alembic environment configuration
│   ├── script.py.mako       # Migration script template
│   └── versions/            # Individual migration files
├── tests/                   # Test files
│   ├── __init__.py
│   ├── test_auth.py         # Authentication tests
│   ├── test_jwt.py          # JWT validation tests
│   ├── test_database.py     # Database connectivity tests
│   ├── test_todo_persistence.py  # Todo persistence tests
│   └── test_user_isolation.py    # User isolation tests
├── .env.example             # Example environment variables
├── .gitignore               # Git ignore patterns
├── alembic.ini              # Alembic configuration
├── pyproject.toml           # Project dependencies and metadata
├── README.md                # Setup and usage instructions
└── test_database_connectivity.py  # Database connectivity test
```

## Development

### Adding Dependencies
When adding new dependencies, update the `pyproject.toml` file and run:
```bash
uv sync  # To update the lock file and install new dependencies
```

### Running with Auto-reload
For development with auto-reload:
```bash
cd src
uv run uvicorn main:app --reload
```

### Environment Configuration
The application uses Pydantic Settings to manage configuration. Settings can be provided via:
- Environment variables
- `.env` file in the backend directory
- Default values in the Settings class

## Configuration

### Environment Variables
- `DATABASE_URL`: PostgreSQL connection string
- `JWT_SECRET`: Secret key for JWT token generation (min 32 chars)
- `BETTER_AUTH_SECRET`: Secret key for authentication (shared with frontend)
- `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`: Access token expiration time
- `JWT_REFRESH_TOKEN_EXPIRE_HOURS`: Refresh token expiration time
- `ENVIRONMENT`: Development environment (development/production/test)
- `DEBUG`: Enable/disable debug mode
- `NEON_DATABASE_URL`: Optional NeonDB-specific connection string