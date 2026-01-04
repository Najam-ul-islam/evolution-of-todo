# Data Model: Todo Console Application

## Task Entity

### Fields
- **id**: Integer (unique, auto-incrementing)
- **title**: String (required, non-empty)
- **description**: String (optional, nullable)
- **completed**: Boolean (default: false)

### Validation Rules
- Title must not be empty or whitespace-only
- ID must be unique within the application instance
- ID must be positive integer

### State Transitions
- `pending` (completed: false) → `completed` (completed: true) - via mark_complete operation
- `completed` (completed: true) → `pending` (completed: false) - via mark_incomplete operation

## Task Collection
- **tasks**: List/Collection of Task entities
- **next_id**: Integer (tracks next available ID for auto-increment)