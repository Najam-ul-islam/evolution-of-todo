# Quickstart Guide: User Authentication Setup

## Overview
This guide explains how to set up and run the user authentication system with Better Auth and JWT tokens for the Todo application.

## Prerequisites
- Node.js 18+ and npm/yarn/pnpm
- Python 3.11 or higher
- PostgreSQL database (NeonDB recommended)
- pip package manager
- Git

## Frontend Setup (Next.js + Better Auth)

### 1. Navigate to the frontend directory
```bash
cd frontend
```

### 2. Install dependencies
```bash
npm install better-auth react-hook-form zod
# or using yarn
yarn add better-auth react-hook-form zod
```

### 3. Configure Better Auth
Create the Better Auth configuration in `frontend/src/lib/better-auth.js`:

```javascript
import { betterAuth } from "better-auth";

export const auth = betterAuth({
  secret: process.env.BETTER_AUTH_SECRET || "your-super-secret-key-change-in-production",
  database: {
    provider: "postgresql",
    url: process.env.DATABASE_URL || "",
  },
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false, // For simplicity in this implementation
  },
  socialProviders: {
    // No third-party providers as per requirements
  },
  session: {
    expiresIn: 7 * 24 * 60 * 60, // 7 days
    cookie: {
      secure: process.env.NODE_ENV === "production",
      httpOnly: true,
      maxAge: 7 * 24 * 60 * 60, // 7 days
    },
  },
});
```

### 4. Create authentication pages
Set up the signup and signin pages with proper form validation.

### 5. Set up environment variables
Create a `.env.local` file in the frontend directory:
```bash
BETTER_AUTH_SECRET=your-super-secret-key-change-in-production
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
DATABASE_URL=postgresql://username:password@localhost:5432/todo_db
```

## Backend Setup (FastAPI + JWT)

### 1. Navigate to the backend directory
```bash
cd backend
```

### 2. Install authentication dependencies
The required dependencies (python-jose, passlib, bcrypt) should already be in pyproject.toml:
```bash
# Already included in the project dependencies
```

### 3. Set up environment variables
Copy the example environment file:
```bash
cp .env.example .env
```

Edit the `.env` file and set your authentication configuration:
```bash
BETTER_AUTH_SECRET=your-super-secret-key-change-in-production
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60
JWT_REFRESH_TOKEN_EXPIRE_HOURS=24
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/todo_db
```

### 4. Configure JWT secret
Make sure the BETTER_AUTH_SECRET is the same in both frontend and backend environments.

## Running the Applications

### 1. Start the backend server
```bash
# From the backend directory
python -m src.main
# Or using uvicorn directly:
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. Start the frontend server
```bash
# From the frontend directory
npm run dev
# Or using yarn:
yarn dev
```

## Testing the Setup

### 1. Create a new user
- Navigate to the signup page (usually `/signup`)
- Fill in the registration form with valid email and strong password
- Submit the form and verify account creation

### 2. Sign in with the new user
- Navigate to the signin page (usually `/signin`)
- Enter the email and password you registered with
- Verify that you are authenticated and redirected to the dashboard

### 3. Verify JWT functionality
- Check that JWT tokens are issued upon successful login
- Verify that protected endpoints require valid JWT tokens
- Test that expired tokens are properly rejected

### 4. Test user isolation
- Create two different user accounts
- Log in as the first user and create some todos
- Log in as the second user and verify you cannot access the first user's todos

## API Endpoints for Authentication

### Frontend (Better Auth)
- `POST /api/auth/register` - User registration
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout
- `GET /api/auth/me` - Get current user info

### Backend (JWT validation)
- `GET /api/v2/users/{user_id}/tasks` - Requires valid JWT token
- `POST /api/v2/users/{user_id}/tasks` - Requires valid JWT token
- `PUT /api/v2/users/{user_id}/tasks/{task_id}` - Requires valid JWT token
- `DELETE /api/v2/users/{user_id}/tasks/{task_id}` - Requires valid JWT token

## Troubleshooting

### Common Issues

#### JWT Validation Errors
- Verify that BETTER_AUTH_SECRET is identical in both frontend and backend
- Check that JWT tokens are properly formatted in requests
- Ensure the Authorization header format is: `Bearer <token>`

#### Database Connection Issues
- Verify your DATABASE_URL is correctly formatted
- Check that your PostgreSQL server is running
- Ensure the database credentials are correct

#### Cross-Origin Issues
- Make sure your frontend and backend are properly configured for CORS
- Check that the allowed origins match your frontend URL

#### Session Management Problems
- Verify that cookies are being set and sent correctly
- Check that httpOnly and secure flags are properly configured for your environment

## Next Steps

After successful setup:
1. Implement the API endpoints to interact with the authentication system
2. Add user profile management functionality
3. Implement password reset functionality
4. Add additional security measures as needed
5. Monitor authentication logs and security events