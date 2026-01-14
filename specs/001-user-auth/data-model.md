# Data Model: User Authentication with JWT

## Entity: User

### Purpose
Represents a registered user in the Todo application with authentication credentials and profile information.

### Fields
- **id** (String, Primary Key): Unique identifier for the user
- **email** (String, Required, Unique): User's email address for login and communication
- **hashed_password** (String, Required): Securely hashed password using bcrypt
- **created_at** (DateTime): Timestamp when the user account was created
- **updated_at** (DateTime): Timestamp when the user account was last updated
- **is_active** (Boolean): Whether the user account is active (default: true)

### Validation Rules
- Email must be valid email format
- Email must be unique across all users
- Password must meet strength requirements (min 8 characters, with uppercase, lowercase, number)
- created_at and updated_at are automatically managed by the system

### Relationships
- **Todo** (One-to-Many): Each user can have multiple todos
- **Todo** (Many-to-One): Each todo belongs to exactly one user

## Entity: JWT Token

### Purpose
Represents a JSON Web Token for user authentication and session management.

### Fields
- **token** (String, Required): The JWT token string
- **user_id** (String, Required): ID of the user to whom the token belongs
- **expires_at** (DateTime): Expiration timestamp for the token
- **created_at** (DateTime): Timestamp when the token was issued
- **token_type** (String): Type of token (access, refresh)

### Validation Rules
- Token must be a valid JWT format
- User ID must correspond to an existing user
- Expires_at must be in the future
- Token must not be expired when used for authentication

### Relationships
- **User** (Many-to-One): Each token belongs to exactly one user

## Entity: Authentication Session

### Purpose
Tracks active authentication sessions for user management and security monitoring.

### Fields
- **session_id** (String, Primary Key): Unique identifier for the session
- **user_id** (String, Required): ID of the user to whom the session belongs
- **jwt_token** (String, Required): Associated JWT token for the session
- **created_at** (DateTime): Timestamp when the session was created
- **last_accessed** (DateTime): Timestamp of the last activity in the session
- **expires_at** (DateTime): Expiration timestamp for the session
- **device_info** (String, Optional): Information about the device used for authentication
- **ip_address** (String, Optional): IP address of the user at session creation

### Validation Rules
- Session must be associated with a valid user
- Session must have a valid, non-expired JWT token
- Last accessed time must not be in the future
- IP address, if provided, must be in valid format

### Relationships
- **User** (Many-to-One): Each session belongs to exactly one user
- **JWT Token** (Many-to-One): Each session is associated with exactly one JWT token

## Entity: User-Data Relationship

### Purpose
Establishes the ownership relationship between users and their data, ensuring proper data isolation.

### Constraints
- Each todo must be associated with exactly one user
- Users can only access data that belongs to them
- Database-level enforcement of user_id foreign key constraint
- Index on user_id field for efficient querying

### Access Rules
- A user can read, update, and delete only their own data
- A user cannot access data belonging to other users
- Attempts to access other users' data should return 404 (not 403 to avoid information leakage)

## Entity: Authentication Configuration

### Purpose
Defines the configuration parameters for the authentication system.

### Fields
- **BETTER_AUTH_SECRET** (String): Secret key for JWT signing and verification
- **JWT_ACCESS_TOKEN_EXPIRY** (Integer): Expiration time for access tokens in seconds
- **JWT_REFRESH_TOKEN_EXPIRY** (Integer): Expiration time for refresh tokens in seconds
- **PASSWORD_MIN_LENGTH** (Integer): Minimum required password length
- **SESSION_TIMEOUT** (Integer): Session timeout duration in seconds