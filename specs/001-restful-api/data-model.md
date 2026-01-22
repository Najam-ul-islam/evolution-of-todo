# Data Model: RESTful API with JWT Protection

## Entity: JWT Token

### Purpose
- Authenticate users for API access
- Store user identity information
- Enable secure stateless authentication

### Claims Structure
- **sub** (subject): User identifier
- **user_id**: Unique user identifier for data isolation
- **exp** (expiration): Token expiration timestamp
- **iat** (issued at): Token creation timestamp
- **scope**: Permissions associated with the token (optional)

### Validation Rules
- Tokens must not be expired
- Tokens must have valid signature
- user_id must correspond to an existing user

## Entity: Authenticated User Context

### Fields
- **user_id**: Unique identifier from JWT token
- **username**: User's display name (optional)
- **permissions**: User's access permissions
- **token_scopes**: Scopes granted by the JWT token

### Validation Rules
- user_id must be present and valid
- Context must be refreshed if token expires

## Entity: User-Scoped Task Query

### Purpose
- Filter tasks based on authenticated user
- Enforce data isolation between users
- Prevent unauthorized access to other users' data

### Parameters
- **authenticated_user_id**: User ID from JWT token
- **requested_user_id**: User ID from API endpoint
- **task_owner_id**: Owner of the task being accessed

### Validation Rules
- authenticated_user_id must match requested_user_id or task_owner_id
- Requests to other users' data should return 404 (not 403 to avoid information leakage)

## Entity: API Response Structure

### For Success Cases
- **data**: Requested resource or operation result
- **status**: Operation status (success, created, updated, etc.)
- **timestamp**: Time of operation completion

### For Error Cases
- **error_code**: Standardized error code
- **message**: Human-readable error description
- **details**: Additional error details (optional)
- **timestamp**: Time of error occurrence

### Validation Rules
- Success responses must include appropriate HTTP status codes
- Error responses must not reveal sensitive information
- Both success and error responses should be consistent in structure