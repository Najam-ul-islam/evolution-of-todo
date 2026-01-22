# Quickstart Guide: AI Agent Behavior and Tool Orchestration

## Overview

Quickstart guide for setting up and using the AI agent that follows deterministic rules for interpreting user messages, selecting MCP tools, and generating conversational responses.

## Prerequisites

- Python 3.11+
- pip or uv package manager
- OpenAI API key
- PostgreSQL database (or compatible)

## Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Set up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
# Or if using uv:
uv sync
```

### 4. Configure Environment Variables
Create a `.env` file with the following:
```env
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/todo_db
JWT_SECRET=your-super-secret-jwt-key-here-make-it-long-and-random
OPENAI_API_KEY=your-openai-api-key
ENVIRONMENT=development
DEBUG=True
```

### 5. Run Database Migrations
```bash
alembic upgrade head
```

## Usage

### 1. Start the Server
```bash
uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Interact with the AI Agent

#### Example 1: Add a Task
```bash
curl -X POST "http://localhost:8000/api/{user_id}/" \
  -H "Authorization: Bearer {jwt_token}" \
  -H "Content-Type: application/json" \
  -d '{"message": "Add a task to buy groceries"}'
```

#### Example 2: List Tasks
```bash
curl -X POST "http://localhost:8000/api/{user_id}/" \
  -H "Authorization: Bearer {jwt_token}" \
  -H "Content-Type: application/json" \
  -d '{"message": "Show my tasks"}'
```

#### Example 3: Complete a Task
```bash
curl -X POST "http://localhost:8000/api/{user_id}/" \
  -H "Authorization: Bearer {jwt_token}" \
  -H "Content-Type: application/json" \
  -d '{"message": "Mark the meeting task as done"}'
```

### 3. Multi-Step Reasoning Example
The AI agent can handle complex requests requiring multiple tool calls:
```bash
curl -X POST "http://localhost:8000/api/{user_id}/" \
  -H "Authorization: Bearer {jwt_token}" \
  -H "Content-Type: application/json" \
  -d '{"message": "Delete the meeting task"}'
```
This will:
1. Call `list_tasks` to identify the meeting task
2. Call `delete_task` on the identified task
3. Return confirmation to the user

## Configuration

### Intent Classification Rules
The agent follows these deterministic rules for intent classification:

| User Intent Keywords | Required Tool |
|---------------------|---------------|
| Add / remember / create | add_task |
| Show / list / see | list_tasks |
| Done / completed / finished | complete_task |
| Delete / remove / cancel | delete_task |
| Update / change / rename | update_task |

### Response Rules
- Always confirm successful actions
- Use friendly, concise language
- Never expose internal tool schemas
- Never hallucinate task state
- Never invent task IDs

### Error Handling
- If task is ambiguous, request clarification
- If task is missing, explain clearly
- If tool fails, surface a user-safe message

## Testing

### Run Unit Tests
```bash
pytest tests/unit/
```

### Run Integration Tests
```bash
pytest tests/integration/
```

### Run Contract Tests
```bash
pytest tests/contract/
```

## Troubleshooting

### Common Issues

1. **JWT Token Required**
   - Ensure you're logged in and have a valid JWT token
   - Check that the Authorization header is properly formatted

2. **Database Connection Issues**
   - Verify DATABASE_URL in your .env file
   - Ensure PostgreSQL is running and accessible

3. **OpenAI API Issues**
   - Check that OPENAI_API_KEY is set in your .env file
   - Verify API key has proper permissions

4. **Intent Recognition Issues**
   - The agent uses keyword matching for intent classification
   - Use clear, direct language matching the classification rules

### Debugging Tips

1. Check server logs for detailed error information
2. Verify all required environment variables are set
3. Ensure database migrations are up to date
4. Use the `/docs` endpoint to test API calls interactively

## Next Steps

1. Customize intent classification rules for your specific use case
2. Add additional MCP tools as needed
3. Fine-tune response templates for your domain
4. Implement monitoring and observability for production use