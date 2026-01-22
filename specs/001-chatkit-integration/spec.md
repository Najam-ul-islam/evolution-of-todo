# Specification: OpenAI ChatKit Integration for AI-Powered Todo Chatbot

## Intent
Integrate the official **OpenAI ChatKit** as the frontend chat interface for Phase III of the Todo app, enabling natural-language task management via a polished, secure, and stateless UI.

## Context
- Project uses a **monorepo** with `/frontend` (Next.js 16 App Router) and `/backend` (FastAPI).
- Authentication is handled by **Better Auth** with JWT tokens.
- The backend exposes a **stateless chat endpoint**: `POST /api/{user_id}/chat`.
- This feature belongs to **Phase III** and must be implemented using **Spec-Driven Development** with **Claude Code** and **Spec-Kit Plus**.

## User Scenarios & Testing

### Primary User Flow
1. User navigates to `/chat` page
2. User sees ChatKit UI with conversation history if `conversation_id` exists
3. User types "Add a task to call mom" in the chat input
4. System processes the message and creates a task in the database
5. User sees confirmation response from the system
6. On page reload, conversation persists via `conversation_id`

### Secondary Flows
- User starts a new conversation without a `conversation_id`
- User returns to an existing conversation with a `conversation_id`
- User receives error messages when invalid commands are sent

### Edge Cases
- Invalid JWT tokens result in authentication errors
- Network failures during message sending
- Invalid conversation IDs return to a new conversation state

## Functional Requirements

### FR1: ChatKit Installation
- The system shall install `@openai/chatkit` in the `/frontend` directory
- The package version shall be ≥ 0.1.0
- Dependencies shall be properly configured for Next.js 16

### FR2: Chat Page Implementation
- The system shall create a page at `/frontend/app/chat/page.tsx`
- The page shall render the `<ChatKit>` component
- The page shall not include any custom chat components outside of ChatKit

### FR3: Message Sending Handler
- The system shall implement an `onSendMessage` handler
- The handler shall fetch the authenticated `user_id` from Better Auth session
- The handler shall send `{ message, conversation_id? }` to `POST /api/${user_id}/chat`
- The handler shall include `Authorization: Bearer <JWT>` header with valid token
- The handler shall return `{ response, conversation_id }` to ChatKit

### FR4: Domain Configuration
- The system shall configure domain key via `NEXT_PUBLIC_OPENAI_DOMAIN_KEY`
- The configuration shall be available in `.env.local` file
- The domain key shall be properly set for both localhost and Vercel deployments

### FR5: Conversation Persistence
- The system shall restore conversation history when `conversation_id` is present
- The system shall maintain conversation continuity across page reloads
- The system shall create a new conversation when no `conversation_id` is provided

### FR6: Documentation Updates
- The system shall update `README.md` with OpenAI domain allowlist instructions
- Instructions shall include steps for Vercel deployment
- Documentation shall be clear and actionable

## Success Criteria

### Quantitative Metrics
- 100% of users can access the ChatKit UI when visiting `/chat`
- 95% of natural language commands result in appropriate database changes
- Page load time under 3 seconds for conversation restoration
- 99% uptime for the chat endpoint during peak usage

### Qualitative Measures
- Users report high satisfaction with natural language task management
- Conversations persist reliably across browser sessions
- Error handling provides clear feedback to users
- Authentication seamlessly integrates with the chat experience

## Key Entities

### User Session
- Authentication token (JWT)
- User identity (`user_id`)
- Session validity

### Conversation
- Unique `conversation_id`
- Message history
- Timestamps
- User association

### Messages
- User input text
- System responses
- Metadata (timestamps, sender type)

## Dependencies & Assumptions

### Dependencies
- Better Auth session availability in Next.js client context
- Backend `/api/{user_id}/chat` endpoint already implemented
- JWT token issuance by Better Auth
- OpenAI ChatKit SDK availability and stability

### Assumptions
- The backend chat endpoint properly handles natural language processing
- Better Auth provides reliable session management in Next.js App Router
- OpenAI ChatKit is compatible with Next.js 16 App Router
- Network connectivity remains stable for real-time messaging

## Non-Goals
- Voice input functionality
- Streaming responses
- Custom theming beyond ChatKit defaults
- Multi-user chat capabilities
- Offline message synchronization

## Constraints
- Must use only official OpenAI ChatKit components
- All requests must include valid JWT authentication
- Solution must work on localhost and *.vercel.app domains
- No custom chat UI components outside of ChatKit
- Stateless operation between requests