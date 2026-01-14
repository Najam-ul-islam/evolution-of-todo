# Backend Quickstart Guide

## Prerequisites

- Python 3.11 or higher
- uv package manager
- Access to NeonDB PostgreSQL instance

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

### 3. Install dependencies using uv
```bash
uv venv  # Creates a virtual environment
source .venv/bin/activate  # Activate the virtual environment (Linux/Mac)
# On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
# Or if using pyproject.toml: uv sync
```

### 4. Set up environment variables
Copy the example environment file and configure your settings:
```bash
cp .env.example .env
```

Edit the `.env` file with your specific configuration:
- `DATABASE_URL`: PostgreSQL connection string for your NeonDB instance
- `JWT_SECRET`: Secure random string for JWT token signing (at least 32 characters)

### 5. Run the application
```bash
cd src
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### 6. Run tests
```bash
cd backend
pytest
```

## API Endpoints

Once running, the API will be available at the following endpoints:
- `GET /` - Health check endpoint
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation (ReDoc)

## Project Structure Overview

```
backend/
├── src/
│   ├── main.py              # Application entry point
│   ├── config/              # Configuration and settings
│   │   └── settings.py
│   ├── models/              # SQLModel database models
│   │   └── todo.py
│   ├── api/                 # API route definitions
│   │   └── v1/
│   │       └── router.py
│   └── utils/               # Utility functions
│       └── database.py
├── tests/                   # Test files
├── .env.example             # Example environment variables
├── pyproject.toml           # Project dependencies and metadata
└── README.md                # Setup and usage instructions
```

## Configuration Details

The application uses Pydantic Settings for configuration management. Environment variables are loaded from the `.env` file or system environment variables.

Key configuration options:
- `DATABASE_URL`: PostgreSQL connection string
- `ENVIRONMENT`: development, production, or test
- `DEBUG`: Enable/disable debug mode
- `JWT_SECRET`: Secret key for JWT token generation