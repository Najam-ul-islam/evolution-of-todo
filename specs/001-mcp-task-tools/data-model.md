# Data Model: MCP Task Management Tools

## Entity: Task

**Description**: Represents a user's task with properties including ID, user association, title, description, and status (pending/completed).

**Fields**:
- `id`: Integer (Primary Key) - Unique identifier for the task
- `user_id`: String - Foreign key linking to the user who owns this task
- `title`: String - Title of the task
- `description`: String (Optional) - Detailed description of the task
- `status`: String (Enum: "pending", "completed") - Current status of the task
- `created_at`: DateTime - Timestamp when the task was created
- `updated_at`: DateTime - Timestamp when the task was last updated

**Validation Rules**:
- `user_id` must exist in the users table
- `title` must not be empty
- `status` must be either "pending" or "completed"
- `created_at` is automatically set when record is created
- `updated_at` is automatically updated when record is modified

## Entity: User

**Description**: Represents a system user with unique identifier and associated tasks.

**Fields**:
- `id`: String (Primary Key) - Unique identifier for the user
- `created_at`: DateTime - Timestamp when the user was created
- `updated_at`: DateTime - Timestamp when the user was last updated

**Validation Rules**:
- `id` must be unique
- `created_at` is automatically set when record is created

## Entity: ToolCall

**Description**: Represents an invocation of an MCP tool with parameters and response data.

**Fields**:
- `id`: Integer (Primary Key) - Unique identifier for the tool call
- `tool_name`: String - Name of the tool that was called
- `parameters`: JSON - Parameters passed to the tool
- `result`: JSON - Result returned by the tool
- `user_id`: String - ID of the user who initiated the tool call
- `created_at`: DateTime - Timestamp when the tool call was made

**Validation Rules**:
- `tool_name` must be one of the valid MCP tools
- `user_id` must exist in the users table
- `created_at` is automatically set when record is created

## Relationships

- **User → Tasks**: One-to-Many relationship
  - A user can have multiple tasks
  - Tasks are filtered by user_id for access control

- **User → ToolCalls**: One-to-Many relationship (optional for audit trail)
  - A user can make multiple tool calls
  - Tool calls are associated with the user who initiated them

## State Transitions

- **Task**:
  - Created with status "pending" when add_task tool is called
  - Updated to "completed" when complete_task tool is called
  - Cannot transition back from "completed" to "pending" through MCP tools

## Indexes

- `tasks.user_id` - For efficient user-specific queries
- `tasks.status` - For efficient status-based filtering
- `tool_calls.user_id` - For efficient audit queries per user
- `tool_calls.tool_name` - For efficient tool usage analytics