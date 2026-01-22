# Quickstart Guide: Persistent Storage Setup

## Overview
This guide explains how to set up and run the persistent storage system using Neon PostgreSQL for the Todo application.

## Prerequisites
- Python 3.11 or higher
- PostgreSQL database (NeonDB recommended)
- pip package manager
- Git

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd evolution-of-todo/backend
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -e .
# Or if you need development dependencies:
pip install -e ".[dev]"
```

### 4. Configure Environment Variables
Copy the example environment file:
```bash
cp .env.example .env
```

Edit the `.env` file and set your database configuration:
```bash
DATABASE_URL=postgresql+asyncpg://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname?sslmode=require
```

### 5. Run Database Migrations
```bash
# Navigate to the backend directory
cd backend

# Run the initial migration to create tables
alembic upgrade head
```

### 6. Start the Application
```bash
# From the backend directory
python -m src.main
# Or using uvicorn directly:
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

## Testing the Setup

### 1. Verify Database Connection
Run the database connectivity test:
```bash
python test_database_connectivity.py
```

### 2. Run Unit Tests
```bash
pytest tests/test_todo_persistence.py
```

### 3. API Testing
Once the application is running, you can test the persistent storage:

```bash
# Create a todo (using the API endpoints once implemented)
curl -X POST http://localhost:8000/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Todo", "description": "This should persist", "completed": false}'
```

## Database Migration Guide

### Initial Setup
When setting up the database for the first time:
```bash
# Generate the initial migration (if not already created)
alembic revision --autogenerate -m "Initial todo model with user_id"

# Apply the migration
alembic upgrade head
```

### Adding New Migrations
When you need to modify the database schema:
```bash
# Generate a new migration based on model changes
alembic revision --autogenerate -m "Description of changes"

# Review the generated migration file in alembic/versions/

# Apply the migration
alembic upgrade head
```

### Rolling Back Migrations
If you need to roll back:
```bash
# Roll back to the previous version
alembic downgrade -1

# Or roll back to a specific version
alembic downgrade <revision_id>
```

## Troubleshooting

### Common Issues

#### Database Connection Issues
- Verify your `DATABASE_URL` is correctly formatted
- Check that your NeonDB instance is running
- Ensure your IP address is whitelisted if using NeonDB

#### Migration Issues
- If migrations fail, check the alembic configuration
- Ensure your models match the expected database schema
- Run `alembic current` to check the current migration state

#### Environment Variables
- Make sure all required environment variables are set
- Check that `.env` file is properly loaded

## Integration with Existing System

The persistent storage system is designed to integrate seamlessly with the existing Todo application:

1. The updated Todo model includes a `user_id` field for proper isolation
2. All CRUD operations now persist data to PostgreSQL
3. User isolation is enforced at the database level
4. Existing API endpoints will work with the persistent storage

## Next Steps

After successful setup:
1. Implement the API endpoints to interact with the persistent storage
2. Add user authentication to properly assign user_ids
3. Test multi-user isolation functionality
4. Monitor database performance and optimize as needed