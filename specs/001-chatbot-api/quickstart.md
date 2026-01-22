# Quickstart Guide: Conversational Chatbot API

## Overview

This guide provides instructions for setting up and running the Conversational Chatbot API that allows users to interact with the Todo system using natural language.

## Prerequisites

- Python 3.11 or higher
- PostgreSQL database (or compatible)
- OpenAI API key
- Poetry or pip for dependency management

## Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Install Dependencies

Using Poetry:
```bash
poetry install
poetry shell
```

Or using pip:
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file in the project root with the following variables:

```env
DATABASE_URL=postgresql://username:password@localhost/dbname
OPENAI_API_KEY=your_openai_api_key_here
SECRET_KEY=your_secret_key_for_jwt
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 4. Database Setup

Run database migrations to create the necessary tables:

```bash
# If using alembic for migrations
alembic upgrade head

# Or run the initialization script
python -c "from src.db.init_db import init_db; init_db()"
```

### 5. Start the Server

```bash
uvicorn src.main:app --reload --port 8000
```

## API Usage

### Authentication

All API requests require a valid JWT token in the Authorization header:

```
Authorization: Bearer <jwt-token>
```

### Making Chat Requests

Send a POST request to `/api/{user_id}/chat`:

```bash
curl -X POST http://localhost:8000/api/123/chat \
  -H "Authorization: Bearer <jwt-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": 456,
    "message": "Add a task to buy groceries for tomorrow"
  }'
```

#### Starting a New Conversation

Omit the `conversation_id` to start a new conversation:

```bash
curl -X POST http://localhost:8000/api/123/chat \
  -H "Authorization: Bearer <jwt-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Add a task to buy groceries for tomorrow"
  }'
```

## API Response Format

The API returns responses in the following format:

```json
{
  "conversation_id": 456,
  "response": "I've added the task 'buy groceries for tomorrow' to your todo list.",
  "tool_calls": [
    {
      "tool_name": "add_todo_item",
      "tool_input": {
        "task": "buy groceries for tomorrow"
      },
      "result": {
        "success": true,
        "todo_id": 789
      }
    }
  ]
}
```

## Testing

Run the tests to verify the setup:

```bash
# Unit tests
pytest tests/unit/

# Integration tests
pytest tests/integration/

# All tests
pytest
```

## Development

### Adding New Tools

To add new tools that the AI agent can use:

1. Create a new service function in `src/services/`
2. Register the function with the OpenAI Agent
3. Update the API contract documentation if needed

### Database Models

The API uses the following database models:

- `Conversation`: Stores conversation metadata
- `Message`: Stores individual messages in conversations
- `ToolCall`: Stores records of tools called by the AI agent

## Troubleshooting

### Common Issues

- **JWT Token Expiry**: Refresh your token if you receive 401 errors
- **Database Connection**: Verify your DATABASE_URL is correct
- **OpenAI API Issues**: Check that your OPENAI_API_KEY is valid and has sufficient quota
- **Conversation Persistence**: Ensure database migrations are applied correctly