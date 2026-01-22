# Data Model: Conversational Chatbot API

## Entity: Conversation

**Description**: Represents a chat session between a user and the AI agent, containing a sequence of messages and associated metadata.

**Fields**:
- `id`: Integer (Primary Key) - Unique identifier for the conversation
- `user_id`: Integer - Foreign key linking to the user who owns this conversation
- `created_at`: DateTime - Timestamp when the conversation was initiated
- `updated_at`: DateTime - Timestamp when the conversation was last modified

**Validation Rules**:
- `user_id` must exist in the users table
- `created_at` is automatically set when record is created
- `updated_at` is automatically updated when record is modified

## Entity: Message

**Description**: Represents an individual exchange in a conversation, including the sender (user or assistant), timestamp, and content.

**Fields**:
- `id`: Integer (Primary Key) - Unique identifier for the message
- `conversation_id`: Integer - Foreign key linking to the parent conversation
- `role`: String (Enum: "user", "assistant") - Identifies the sender of the message
- `content`: Text - The actual content of the message
- `created_at`: DateTime - Timestamp when the message was created

**Validation Rules**:
- `conversation_id` must exist in the conversations table
- `role` must be either "user" or "assistant"
- `content` must not be empty
- `created_at` is automatically set when record is created

## Entity: ToolCall

**Description**: Represents an action performed by the AI agent during processing, including the tool name and parameters.

**Fields**:
- `id`: Integer (Primary Key) - Unique identifier for the tool call
- `message_id`: Integer - Foreign key linking to the message that triggered this tool call
- `tool_name`: String - Name of the tool that was called
- `tool_input`: JSON - Parameters passed to the tool
- `result`: JSON - Result returned by the tool (nullable)
- `created_at`: DateTime - Timestamp when the tool call was recorded

**Validation Rules**:
- `message_id` must exist in the messages table
- `tool_name` must not be empty
- `tool_input` must be valid JSON

## Relationships

- **Conversation → Messages**: One-to-Many relationship
  - A conversation can have multiple messages
  - Messages are deleted when their parent conversation is deleted (CASCADE)
  - Messages are ordered by `created_at` timestamp

- **Message → ToolCalls**: One-to-Many relationship
  - A message can trigger multiple tool calls
  - Tool calls are deleted when their parent message is deleted (CASCADE)

## State Transitions

- **Conversation**:
  - Created when a new chat session begins
  - Updated when new messages are added to the conversation
  - Remains active until explicitly deleted or archived

- **Message**:
  - Created when either user or assistant sends a message
  - Immutable after creation (no updates allowed)
  - Automatically linked to a conversation

- **ToolCall**:
  - Created when an AI agent invokes a tool during message processing
  - Optionally updated with results when the tool execution completes
  - Linked to the message that triggered the tool call

## Indexes

- `conversations.user_id` - For efficient user-specific queries
- `messages.conversation_id` - For efficient conversation history retrieval
- `messages.created_at` - For chronological ordering of messages
- `tool_calls.message_id` - For efficient tool call retrieval per message