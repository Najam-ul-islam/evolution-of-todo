# API Contracts: Frontend Interface (Standalone Prototype)

## Overview
This document defines the API contracts for the todo management frontend. Since this is a prototype with mock APIs, the contracts represent the expected interface that will be implemented in future phases. The mock implementations will follow these contracts to ensure seamless transition to real API calls.

## Authentication API Contracts

### Sign Up
**Endpoint**: `POST /api/auth/signup`
**Purpose**: Register a new user account

#### Request
```json
{
  "email": "string (required)",
  "password": "string (required, min 8 characters)",
  "name": "string (required)"
}
```

#### Response (Success)
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "string",
      "email": "string",
      "name": "string",
      "createdAt": "ISO date string"
    },
    "session": {
      "token": "string",
      "expiresAt": "ISO date string"
    }
  }
}
```

#### Response (Error)
```json
{
  "success": false,
  "error": {
    "message": "string",
    "code": "AUTH_VALIDATION_ERROR | USER_EXISTS"
  }
}
```

### Sign In
**Endpoint**: `POST /api/auth/signin`
**Purpose**: Authenticate an existing user

#### Request
```json
{
  "email": "string (required)",
  "password": "string (required)"
}
```

#### Response (Success)
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "string",
      "email": "string",
      "name": "string",
      "createdAt": "ISO date string"
    },
    "session": {
      "token": "string",
      "expiresAt": "ISO date string"
    }
  }
}
```

#### Response (Error)
```json
{
  "success": false,
  "error": {
    "message": "string",
    "code": "AUTH_CREDENTIALS_ERROR | USER_NOT_FOUND"
  }
}
```

### Sign Out
**Endpoint**: `POST /api/auth/logout`
**Purpose**: End the current user session

#### Request
```json
{
  "headers": {
    "Authorization": "Bearer {token}"
  }
}
```

#### Response (Success)
```json
{
  "success": true,
  "data": {
    "message": "Successfully signed out"
  }
}
```

#### Response (Error)
```json
{
  "success": false,
  "error": {
    "message": "string",
    "code": "AUTH_UNAUTHORIZED"
  }
}
```

### Get Current User
**Endpoint**: `GET /api/auth/me`
**Purpose**: Retrieve current authenticated user information

#### Request
```json
{
  "headers": {
    "Authorization": "Bearer {token}"
  }
}
```

#### Response (Success)
```json
{
  "success": true,
  "data": {
    "user": {
      "id": "string",
      "email": "string",
      "name": "string",
      "createdAt": "ISO date string"
    }
  }
}
```

#### Response (Error)
```json
{
  "success": false,
  "error": {
    "message": "string",
    "code": "AUTH_UNAUTHORIZED"
  }
}
```

## Todo API Contracts

### Get Todos
**Endpoint**: `GET /api/todos`
**Purpose**: Retrieve all todos for the authenticated user

#### Request
```json
{
  "headers": {
    "Authorization": "Bearer {token}"
  },
  "query": {
    "completed": "boolean (optional)",
    "priority": "'low' | 'medium' | 'high' (optional)",
    "page": "number (optional, default: 1)",
    "limit": "number (optional, default: 20)",
    "sortBy": "'createdAt' | 'updatedAt' | 'dueDate' (optional, default: 'createdAt')",
    "sortOrder": "'asc' | 'desc' (optional, default: 'desc')"
  }
}
```

#### Response (Success)
```json
{
  "success": true,
  "data": [
    {
      "id": "string",
      "title": "string",
      "description": "string",
      "completed": "boolean",
      "priority": "'low' | 'medium' | 'high'",
      "dueDate": "ISO date string | null",
      "createdAt": "ISO date string",
      "updatedAt": "ISO date string",
      "userId": "string"
    }
  ],
  "pagination": {
    "page": "number",
    "limit": "number",
    "total": "number",
    "totalPages": "number"
  }
}
```

#### Response (Error)
```json
{
  "success": false,
  "error": {
    "message": "string",
    "code": "AUTH_UNAUTHORIZED"
  }
}
```

### Create Todo
**Endpoint**: `POST /api/todos`
**Purpose**: Create a new todo for the authenticated user

#### Request
```json
{
  "headers": {
    "Authorization": "Bearer {token}"
  },
  "body": {
    "title": "string (required)",
    "description": "string (optional)",
    "priority": "'low' | 'medium' | 'high' (optional, default: 'medium')",
    "dueDate": "ISO date string | null (optional)"
  }
}
```

#### Response (Success)
```json
{
  "success": true,
  "data": {
    "id": "string",
    "title": "string",
    "description": "string",
    "completed": "false",
    "priority": "'low' | 'medium' | 'high'",
    "dueDate": "ISO date string | null",
    "createdAt": "ISO date string",
    "updatedAt": "ISO date string",
    "userId": "string"
  }
}
```

#### Response (Error)
```json
{
  "success": false,
  "error": {
    "message": "string",
    "code": "AUTH_UNAUTHORIZED | VALIDATION_ERROR"
  }
}
```

### Update Todo
**Endpoint**: `PUT /api/todos/{id}`
**Purpose**: Update an existing todo

#### Request
```json
{
  "headers": {
    "Authorization": "Bearer {token}"
  },
  "params": {
    "id": "string (required)"
  },
  "body": {
    "title": "string (optional)",
    "description": "string (optional)",
    "completed": "boolean (optional)",
    "priority": "'low' | 'medium' | 'high' (optional)",
    "dueDate": "ISO date string | null (optional)"
  }
}
```

#### Response (Success)
```json
{
  "success": true,
  "data": {
    "id": "string",
    "title": "string",
    "description": "string",
    "completed": "boolean",
    "priority": "'low' | 'medium' | 'high'",
    "dueDate": "ISO date string | null",
    "createdAt": "ISO date string",
    "updatedAt": "ISO date string",
    "userId": "string"
  }
}
```

#### Response (Error)
```json
{
  "success": false,
  "error": {
    "message": "string",
    "code": "AUTH_UNAUTHORIZED | VALIDATION_ERROR | TODO_NOT_FOUND"
  }
}
```

### Delete Todo
**Endpoint**: `DELETE /api/todos/{id}`
**Purpose**: Delete a todo

#### Request
```json
{
  "headers": {
    "Authorization": "Bearer {token}"
  },
  "params": {
    "id": "string (required)"
  }
}
```

#### Response (Success)
```json
{
  "success": true,
  "data": {
    "message": "Todo deleted successfully"
  }
}
```

#### Response (Error)
```json
{
  "success": false,
  "error": {
    "message": "string",
    "code": "AUTH_UNAUTHORIZED | TODO_NOT_FOUND"
  }
}
```

### Toggle Todo Completion
**Endpoint**: `PATCH /api/todos/{id}/toggle-completion`
**Purpose**: Toggle the completion status of a todo

#### Request
```json
{
  "headers": {
    "Authorization": "Bearer {token}"
  },
  "params": {
    "id": "string (required)"
  }
}
```

#### Response (Success)
```json
{
  "success": true,
  "data": {
    "id": "string",
    "completed": "boolean"
  }
}
```

#### Response (Error)
```json
{
  "success": false,
  "error": {
    "message": "string",
    "code": "AUTH_UNAUTHORIZED | TODO_NOT_FOUND"
  }
}
```

## Error Codes

### Authentication Errors
- `AUTH_CREDENTIALS_ERROR`: Invalid email/password combination
- `AUTH_UNAUTHORIZED`: Missing or invalid authentication token
- `AUTH_TOKEN_EXPIRED`: Authentication token has expired
- `USER_NOT_FOUND`: User does not exist
- `USER_EXISTS`: User with email already exists
- `AUTH_VALIDATION_ERROR`: Validation error in authentication request

### Validation Errors
- `VALIDATION_ERROR`: Generic validation error
- `MISSING_REQUIRED_FIELD`: Required field is missing
- `INVALID_FORMAT`: Field value has incorrect format
- `VALUE_TOO_LONG`: Field value exceeds maximum length
- `VALUE_TOO_SHORT`: Field value is below minimum length

### Resource Errors
- `TODO_NOT_FOUND`: Todo with specified ID does not exist
- `RESOURCE_CONFLICT`: Attempting to create duplicate resource
- `INSUFFICIENT_PERMISSIONS`: User lacks permission for operation

### System Errors
- `INTERNAL_SERVER_ERROR`: Unexpected server error
- `SERVICE_UNAVAILABLE`: Service temporarily unavailable
- `RATE_LIMIT_EXCEEDED`: Too many requests from client

## Headers

### Request Headers
- `Authorization`: Bearer token for authenticated requests
- `Content-Type`: `application/json` for JSON payloads
- `Accept`: `application/json` for JSON responses

### Response Headers
- `Content-Type`: `application/json`
- `X-Request-ID`: Unique identifier for request tracing
- `Cache-Control`: Appropriate caching directives

## Response Status Codes

### Success Responses
- `200`: OK - Request successful
- `201`: Created - Resource successfully created
- `204`: No Content - Request successful, no content to return

### Client Error Responses
- `400`: Bad Request - Invalid request format
- `401`: Unauthorized - Authentication required
- `403`: Forbidden - Insufficient permissions
- `404`: Not Found - Resource does not exist
- `409`: Conflict - Resource conflict
- `422`: Unprocessable Entity - Validation error
- `429`: Too Many Requests - Rate limit exceeded

### Server Error Responses
- `500`: Internal Server Error - Unexpected server error
- `503`: Service Unavailable - Service temporarily unavailable

## Future Integration Notes

### JWT Implementation Points
- **TODO**: Replace mock tokens with real JWT implementation
- **TODO**: Add refresh token mechanism
- **TODO**: Implement proper token expiration handling
- **TODO**: Add token blacklisting for logout

### API Endpoint Integration Points
- **TODO**: Replace mock API base URL with real backend URL
- **TODO**: Add proper error handling for network failures
- **TODO**: Implement retry mechanisms for failed requests
- **TODO**: Add request/response logging for debugging

### Security Enhancement Points
- **TODO**: Implement CSRF protection
- **TODO**: Add request rate limiting
- **TODO**: Implement proper input sanitization
- **TODO**: Add API monitoring and alerting