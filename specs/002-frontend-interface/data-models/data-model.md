# Data Model: Frontend Interface (Standalone Prototype)

## Overview
This document defines the core data entities and their relationships for the todo management frontend. The data model is designed to support both the current mock implementation and future backend integration.

## Core Entities

### 1. User Entity
Represents the authenticated user in the system.

#### Fields:
- `id`: string - Unique identifier for the user
- `email`: string - User's email address (used for authentication)
- `name`: string - User's display name
- `createdAt`: Date - Timestamp when user account was created
- `updatedAt`: Date - Timestamp when user account was last updated
- `isEmailVerified`: boolean - Whether the user's email has been verified

#### Validation Rules:
- `email`: Must be a valid email format
- `name`: Required, minimum 1 character, maximum 100 characters
- `id`: Auto-generated UUID format

#### State Transitions:
- New User → Email Verified
- Active User → Deleted (soft delete)

### 2. Todo Entity
Represents a todo item owned by a user.

#### Fields:
- `id`: string - Unique identifier for the todo
- `title`: string - Title/description of the todo
- `description`: string - Optional detailed description
- `completed`: boolean - Whether the todo is completed
- `priority`: 'low' | 'medium' | 'high' - Priority level
- `dueDate`: Date | null - Optional deadline for the todo
- `createdAt`: Date - Timestamp when todo was created
- `updatedAt`: Date - Timestamp when todo was last updated
- `userId`: string - Reference to the owner user

#### Validation Rules:
- `title`: Required, minimum 1 character, maximum 255 characters
- `description`: Optional, maximum 1000 characters
- `priority`: Must be one of 'low', 'medium', 'high'
- `userId`: Must reference an existing user

#### State Transitions:
- Active → Completed
- Completed → Active (toggle back)

### 3. Session Entity (Client-side)
Represents the user's authentication state stored locally.

#### Fields:
- `userId`: string - Reference to the authenticated user
- `token`: string - Authentication token (simulated for prototype)
- `expiresAt`: Date - Expiration timestamp
- `createdAt`: Date - Session creation time

## Relationships

### User → Todo (One-to-Many)
- A user can own multiple todos
- Foreign key: `todos.userId` references `users.id`
- Cascade delete: When user is deleted, associated todos are also deleted

## TypeScript Interfaces

### User Interface
```typescript
interface User {
  id: string;
  email: string;
  name: string;
  createdAt: Date;
  updatedAt: Date;
  isEmailVerified: boolean;
}
```

### Todo Interface
```typescript
interface Todo {
  id: string;
  title: string;
  description: string;
  completed: boolean;
  priority: 'low' | 'medium' | 'high';
  dueDate: Date | null;
  createdAt: Date;
  updatedAt: Date;
  userId: string;
}
```

### Session Interface
```typescript
interface Session {
  userId: string;
  token: string;
  expiresAt: Date;
  createdAt: Date;
}
```

### API Response Types
```typescript
interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: {
    message: string;
    code?: string;
    details?: any;
  };
}

interface PaginatedResponse<T> extends ApiResponse<T[]> {
  pagination: {
    page: number;
    limit: number;
    total: number;
    totalPages: number;
  };
}
```

## Mock Data Examples

### Sample User
```json
{
  "id": "user_123",
  "email": "john.doe@example.com",
  "name": "John Doe",
  "createdAt": "2026-01-10T10:00:00.000Z",
  "updatedAt": "2026-01-10T10:00:00.000Z",
  "isEmailVerified": true
}
```

### Sample Todo
```json
{
  "id": "todo_456",
  "title": "Complete project proposal",
  "description": "Finish writing and review the Q1 project proposal document",
  "completed": false,
  "priority": "high",
  "dueDate": "2026-01-15T23:59:59.000Z",
  "createdAt": "2026-01-10T09:00:00.000Z",
  "updatedAt": "2026-01-10T09:00:00.000Z",
  "userId": "user_123"
}
```

## Business Logic

### Todo Operations
1. **Create**: User can create a new todo with title, optional description, priority, and due date
2. **Read**: User can view all their todos, filtered by completion status, priority, or date range
3. **Update**: User can modify todo properties including completion status
4. **Delete**: User can permanently delete a todo
5. **Toggle Completion**: User can mark a todo as completed/incomplete

### User Operations
1. **Sign Up**: User can register with email and password
2. **Sign In**: User can authenticate with email and password
3. **Sign Out**: User can end their session
4. **Profile Update**: User can update their profile information

## Constraints and Indexes

### Database Constraints
- Unique constraint on User.email
- Foreign key constraint from Todo.userId to User.id
- Check constraint on Todo.priority values

### Indexes
- Index on User.email for fast authentication lookup
- Index on Todo.userId for efficient todo retrieval by user
- Index on Todo.completed for filtering completed todos
- Composite index on Todo.userId and Todo.completed for combined queries

## Data Flow

### Client-Side Data Flow
1. User interacts with UI components
2. Components call service layer functions
3. Service layer (currently mock) returns data
4. React state/context updates components
5. Components re-render based on new state

### Future Backend Integration
1. User interacts with UI components
2. Components call service layer functions
3. Service layer makes API calls to backend
4. Backend validates, processes, and returns data
5. Service layer returns data to components
6. React state/context updates components
7. Components re-render based on new state

## Validation Strategy

### Client-Side Validation
- Form validation using schema validation libraries
- Real-time validation feedback
- Prevention of invalid data submission

### Server-Side Validation (Future)
- Comprehensive data validation
- Business rule enforcement
- Security validation

## Error Handling

### Data Validation Errors
- Invalid field values
- Missing required fields
- Constraint violations

### Operation Errors
- Network failures
- Unauthorized access attempts
- Data conflicts
- Unexpected server responses