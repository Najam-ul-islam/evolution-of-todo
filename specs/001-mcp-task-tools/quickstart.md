# Quickstart Guide: MCP Task Management Tools

## Overview

This guide provides instructions for setting up and using the MCP Task Management Tools that allow AI agents to safely perform task operations through a controlled, stateless tool interface.

## Prerequisites

- Python 3.11 or higher
- Official MCP SDK
- Access to existing task services (from the backend system)
- Database access (PostgreSQL or compatible)

## Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Install Dependencies

Using uv (recommended):
```bash
uv sync
```

Or using pip:
```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file in the project root with the necessary configuration:

```env
DATABASE_URL=postgresql://username:password@localhost/dbname
MCP_SERVER_HOST=localhost
MCP_SERVER_PORT=8001
LOG_LEVEL=INFO
```

### 4. Database Setup

Ensure the database is properly configured with the required tables:

```bash
# Run database migrations to create required tables
alembic upgrade head
```

## MCP Tool Usage

### Available Tools

#### 1. add_task
Creates a new task for a user.

**Parameters**:
- `user_id` (string, required): The ID of the user creating the task
- `title` (string, required): The title of the task
- `description` (string, optional): A description of the task

**Returns**:
- `task_id`: The ID of the created task
- `status`: The status of the task (usually "pending")
- `title`: The title of the task

#### 2. list_tasks
Lists tasks for a user.

**Parameters**:
- `user_id` (string, required): The ID of the user whose tasks to list
- `status` (string, optional): Filter by status ("all", "pending", "completed")

**Returns**:
- Array of task objects with id, title, description, and status

#### 3. update_task
Updates properties of an existing task.

**Parameters**:
- `user_id` (string, required): The ID of the user who owns the task
- `task_id` (integer, required): The ID of the task to update
- `title` (string, optional): New title for the task
- `description` (string, optional): New description for the task

**Returns**:
- `task_id`: The ID of the updated task
- `status`: The status of the task
- `title`: The title of the task

#### 4. complete_task
Marks a task as completed.

**Parameters**:
- `user_id` (string, required): The ID of the user who owns the task
- `task_id` (integer, required): The ID of the task to complete

**Returns**:
- `task_id`: The ID of the completed task
- `status`: The status of the task ("completed")
- `title`: The title of the task

#### 5. delete_task
Deletes a task.

**Parameters**:
- `user_id` (string, required): The ID of the user who owns the task
- `task_id` (integer, required): The ID of the task to delete

**Returns**:
- `task_id`: The ID of the deleted task
- `status`: The status of the task at time of deletion
- `title`: The title of the task

## Error Handling

The MCP tools return standardized error responses:

- **Task not found**: `{ "error": "TASK_NOT_FOUND", "message": "Task with ID X not found for user Y" }`
- **Unauthorized access**: `{ "error": "UNAUTHORIZED", "message": "User Y does not have access to task X" }`
- **Invalid parameters**: `{ "error": "INVALID_PARAMS", "message": "Parameter Z is required" }`

## Testing

Run the tests to verify the MCP tools are working correctly:

```bash
# Unit tests for individual tools
pytest tests/unit/tools/

# Integration tests for MCP server
pytest tests/integration/mcp/

# All tests
pytest
```

## Development

### Adding New Tools

To add new MCP tools:

1. Define the tool signature and parameters in the tool registry
2. Implement the tool function with proper validation
3. Ensure the tool follows the stateless and user ownership constraints
4. Add appropriate error handling
5. Update the documentation

### Best Practices

- Always validate user ownership before performing operations
- Maintain statelessness between tool calls
- Return machine-readable responses
- Log tool calls for auditability
- Handle errors gracefully without exposing internal details

## Troubleshooting

### Common Issues

- **Database connection errors**: Verify DATABASE_URL is correctly configured
- **Permission errors**: Check that user IDs match task ownership
- **Invalid parameter errors**: Ensure required parameters are provided in the correct format
- **State persistence issues**: Remember that MCP tools must be stateless