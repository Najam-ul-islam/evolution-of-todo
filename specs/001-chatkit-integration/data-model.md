# Data Model: OpenAI ChatKit Integration for Todo Chatbot

## Frontend State Entities

### User Session Entity
- **Entity**: UserSession
- **Fields**:
  - `user_id`: string - Unique identifier for the authenticated user
  - `jwt_token`: string - Authentication token for API calls
  - `session_valid`: boolean - Indicates if the session is currently valid
  - `expires_at`: Date - Expiration timestamp for the JWT token

### Conversation Entity
- **Entity**: Conversation
- **Fields**:
  - `conversation_id`: string - Unique identifier for conversation persistence
  - `messages`: Array<Message> - Collection of messages in the conversation
  - `created_at`: Date - Timestamp when conversation was initiated
  - `updated_at`: Date - Timestamp when conversation was last updated
  - `user_id`: string - Reference to the user who owns this conversation

### Message Entity
- **Entity**: Message
- **Fields**:
  - `id`: string - Unique identifier for the message
  - `content`: string - Text content of the message
  - `sender_type`: enum('user' | 'assistant') - Identifies if message is from user or system
  - `timestamp`: Date - When the message was sent/received
  - `conversation_id`: string - Reference to the conversation this message belongs to

## State Transitions

### User Session Transitions
- `unauthenticated` → `authenticated` (when user logs in)
- `authenticated` → `expired` (when token expires)
- `expired` → `authenticated` (when token is refreshed)

### Conversation Transitions
- `new` → `active` (when first message is sent)
- `active` → `paused` (when user leaves without ending conversation)
- `paused` → `active` (when user returns to conversation)
- `active` → `archived` (when conversation is explicitly ended)

## Validation Rules

### User Session Validation
- `jwt_token` must be a valid JWT format
- `session_valid` must be true when `expires_at` is in the future
- `user_id` must match the user ID in the JWT token

### Conversation Validation
- `conversation_id` must be unique per user
- `messages` array must not exceed 1000 messages
- `created_at` must be before `updated_at`

### Message Validation
- `content` must be between 1 and 4000 characters
- `sender_type` must be either 'user' or 'assistant'
- `timestamp` must be within the last 30 days

## Relationships

### UserSession ↔ Conversation
- One-to-many: One user session can have multiple conversations
- Relationship: `UserSession.user_id` → `Conversation.user_id`

### Conversation ↔ Message
- One-to-many: One conversation contains multiple messages
- Relationship: `Conversation.conversation_id` → `Message.conversation_id`

## State Management

### Client-Side State
- User session information stored in React state/context
- Current conversation ID maintained in component state
- Temporary message history cached in component state before API sync

### Server-Side State
- User sessions managed by Better Auth
- Conversations and messages stored in backend database
- JWT tokens issued and validated by authentication service