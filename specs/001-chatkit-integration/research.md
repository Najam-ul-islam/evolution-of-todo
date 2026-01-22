# Research: OpenAI ChatKit Integration for Todo Chatbot

## R1: Better Auth Session Integration

### Decision
Using Better Auth hooks directly in the client component to access user_id and JWT token.

### Rationale
Better Auth provides React hooks that can be used directly in client components to access the user session. This is the most straightforward approach to get the user context needed for authenticating API calls.

### Alternatives considered
- Using Better Auth hooks directly in client component (selected approach)
- Creating a custom hook to abstract the session access
- Server-side props to pass user data to client

### Findings
Better Auth provides `useSession` hook that returns the current user session including user ID and authentication status. For JWT tokens specifically, we may need to implement a custom API route to issue JWTs or use Better Auth's built-in token management.

## R2: OpenAI ChatKit Configuration

### Decision
Standard ChatKit setup with domain-specific configuration for allowlisting.

### Rationale
OpenAI ChatKit needs to be configured with specific domains that are allowed to use the service. This requires setting up the domain key appropriately for both development (localhost) and production (Vercel) environments.

### Alternatives considered
- Standard ChatKit setup with minimal customization (selected approach)
- Custom ChatKit configuration with domain-specific settings
- Wrapper component approach for additional control

### Findings
ChatKit requires domain allowlisting through an environment variable `NEXT_PUBLIC_OPENAI_DOMAIN_KEY`. This needs to be configured in `.env.local` for development and in Vercel deployment settings for production.

## R3: API Communication Pattern

### Decision
Direct fetch calls from onSendMessage handler with proper authentication headers.

### Rationale
The simplest approach is to make direct API calls from the onSendMessage handler while including the JWT token in the authorization header. This keeps the logic contained within the component and makes the data flow clear.

### Alternatives considered
- Direct fetch calls from onSendMessage handler (selected approach)
- Custom service layer to handle API communication
- Context-based API service for centralized management

### Findings
The onSendMessage handler in ChatKit receives the message content and can be augmented to include authentication headers and conversation ID when making requests to our backend API.

## Additional Research Findings

### Next.js App Router Integration
ChatKit components can be integrated directly into Next.js 16 App Router pages. The client component will need "use client" directive to use React hooks.

### Environment Variables
Environment variables prefixed with NEXT_PUBLIC_ are available in client-side code, which is necessary for the domain key configuration.

### Backend API Compatibility
The existing `/api/{user_id}/chat` endpoint should accept messages and return responses with conversation IDs, which matches the requirements for ChatKit integration.