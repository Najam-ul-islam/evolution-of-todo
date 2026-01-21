# API Contract: Frontend to Backend Communication for ChatKit Integration

## Overview
This document specifies the API contract between the frontend ChatKit component and the backend chat endpoint.

## Endpoint
- **Method**: POST
- **Path**: `/api/{user_id}/chat`
- **Authentication**: Required (JWT token in Authorization header)

## Request

### Headers
```
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

### Path Parameters
| Parameter | Type   | Description                 |
|-----------|--------|-----------------------------|
| user_id   | string | The authenticated user's ID |

### Request Body
```json
{
  "message": "string",
  "conversation_id": "string (optional)"
}
```

#### Fields
- **message** (required): The message content sent by the user
  - Type: string
  - Min length: 1 character
  - Max length: 4000 characters
- **conversation_id** (optional): Identifier for conversation persistence
  - Type: string
  - Format: UUID or similar unique identifier

## Response

### Success Response (200 OK)
```json
{
  "response": "string",
  "conversation_id": "string"
}
```

#### Fields
- **response** (required): The response from the backend/chatbot
  - Type: string
  - Contains the natural language response to the user's message
- **conversation_id** (required): The conversation identifier
  - Type: string
  - Unique identifier for the conversation thread
  - New ID generated for new conversations, existing ID returned for ongoing conversations

### Error Responses

#### 400 Bad Request
Returned when request body is malformed or contains invalid data.

```json
{
  "error": "string",
  "details": "object (optional)"
}
```

#### 401 Unauthorized
Returned when the JWT token is invalid or missing.

```json
{
  "error": "Unauthorized",
  "message": "string"
}
```

#### 403 Forbidden
Returned when the user tries to access a conversation that doesn't belong to them.

```json
{
  "error": "Forbidden",
  "message": "Access to conversation not allowed"
}
```

#### 404 Not Found
Returned when the specified conversation_id doesn't exist.

```json
{
  "error": "Not Found",
  "message": "Conversation not found"
}
```

#### 500 Internal Server Error
Returned when there's an unexpected error on the server.

```json
{
  "error": "Internal Server Error",
  "message": "An unexpected error occurred"
}
```

## Examples

### Example Request
```
POST /api/user123/chat
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "message": "Add a task to buy groceries",
  "conversation_id": "conv-abc123"
}
```

### Example Success Response
```json
{
  "response": "I've added the task 'buy groceries' to your list.",
  "conversation_id": "conv-abc123"
}
```

### Example Error Response
```json
{
  "error": "Unauthorized",
  "message": "Invalid or expired JWT token"
}
```

## Rate Limiting
- Requests are limited to 100 per minute per user
- Exceeded limits return 429 Too Many Requests with retry-after header

## Security Considerations
- JWT tokens must be validated on every request
- User ID in path parameter must match the user ID in the JWT token
- All sensitive data must be properly sanitized
- Input validation must be performed on all request parameters