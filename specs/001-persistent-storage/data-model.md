# Data Model: Persistent Storage with User Isolation

## Entity: Todo

### Purpose
Represents a user's task in the Todo application with full persistence capabilities and user isolation.

### Fields
- **id** (Integer, Primary Key): Unique identifier for the todo item
- **title** (String, Required): Title of the todo task (max 255 characters)
- **description** (String, Optional): Detailed description of the task (max 1000 characters)
- **completed** (Boolean): Whether the task has been completed (default: false)
- **user_id** (String, Required, Indexed): Foreign key identifying the user who owns this todo
- **created_at** (DateTime): Timestamp when the todo was created
- **updated_at** (DateTime): Timestamp when the todo was last updated

### Validation Rules
- Title must be between 1 and 255 characters
- Description, if provided, must be between 1 and 1000 characters
- user_id must be present and valid
- created_at and updated_at are automatically managed by the system

### Relationships
- **User** (Many-to-One): Each todo belongs to exactly one user
- **User** (One-to-Many): Each user can have multiple todos

## Entity: User

### Purpose
Represents a system user who owns multiple todo items with proper data isolation.

### Fields
- **user_id** (String, Primary Key): Unique identifier for the user
- **created_at** (DateTime): Timestamp when the user account was created
- **updated_at** (DateTime): Timestamp when the user account was last updated

### Validation Rules
- user_id must be unique across all users
- user_id must be present and valid

### Relationships
- **Todo** (One-to-Many): Each user can have multiple todos
- **Todo** (Many-to-One): Each todo belongs to exactly one user

## Entity: Todo-User Relationship

### Purpose
Establishes the ownership relationship between todos and users, ensuring proper data isolation.

### Constraints
- Each todo must be associated with exactly one user
- Users can only access todos that belong to them
- Database-level enforcement of user_id foreign key constraint
- Index on user_id field for efficient querying

### Access Rules
- A user can read, update, and delete only their own todos
- A user cannot access todos belonging to other users
- Attempts to access other users' todos should return 404 (not 403 to avoid information leakage)

## Entity: Database Connection Configuration

### Purpose
Defines the configuration parameters for connecting to the Neon PostgreSQL database.

### Fields
- **DATABASE_URL** (String): Full connection string including protocol, host, port, database name, and credentials
- **pool_size** (Integer): Maximum number of connections in the pool
- **pool_timeout** (Integer): Timeout for acquiring a connection from the pool
- **pool_recycle** (Integer): Time after which connections are recycled

### Validation Rules
- DATABASE_URL must follow PostgreSQL connection string format
- pool_size must be a positive integer
- pool_timeout must be a positive integer
- pool_recycle should be set to prevent stale connections

## Entity: Migration State

### Purpose
Tracks the current state of database migrations to ensure schema consistency.

### Fields
- **version** (String): Current migration version identifier
- **applied_at** (DateTime): Timestamp when migration was applied
- **description** (String): Human-readable description of the migration

### Validation Rules
- version must be unique
- applied_at must be a valid timestamp
- Each migration can only be applied once