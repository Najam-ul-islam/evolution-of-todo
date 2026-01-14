# API Contracts

This directory contains the API contract specifications for the Todo application's authentication system.

## Files

- `auth-api.yaml` - OpenAPI 3.0 specification for the authentication API endpoints
  - User registration (`POST /api/auth/register`)
  - User login (`POST /api/auth/login`)
  - User logout (`POST /api/auth/logout`)
  - Get current user (`GET /api/auth/me`)
  - Task management endpoints that require JWT authentication

## Purpose

These contracts define the interface between the frontend and backend applications, ensuring consistent API behavior and enabling independent development of both components. The contracts specify:

- Request/response formats
- Authentication requirements
- Error handling patterns
- Data validation rules
- API versioning strategy

## Usage

These specifications can be used to:
- Generate client SDKs for frontend applications
- Validate API implementations
- Document the API for developers
- Enable contract testing between frontend and backend