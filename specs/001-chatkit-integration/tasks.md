# Tasks: OpenAI ChatKit Integration for Todo Chatbot

**Feature**: OpenAI ChatKit Integration for Todo Chatbot
**Spec**: @specs/001-chatkit-integration/spec.md
**Plan**: @specs/001-chatkit-integration/plan.md
**Date**: 2026-01-21

## Phase 1: Setup

### Goal
Initialize the project with necessary dependencies and configuration for ChatKit integration.

### Independent Test Criteria
- `@openai/chatkit` dependency is installed in frontend
- Environment variables are properly configured for domain key
- Basic project structure is in place

### Implementation Tasks

- [ ] T001 Install @openai/chatkit dependency in /frontend
- [ ] T002 Create .env.local.example with NEXT_PUBLIC_OPENAI_DOMAIN_KEY placeholder

## Phase 2: Foundational

### Goal
Establish the foundational components needed for all user stories: authentication integration and API communication layer.

### Independent Test Criteria
- Better Auth session can be accessed in client component
- API communication layer can make authenticated requests to backend
- JWT tokens are properly included in requests

### Implementation Tasks

- [ ] T003 Create /frontend/lib/auth.ts to extract user_id and jwt from Better Auth session
- [ ] T004 Create /frontend/services/chat-api.ts for authenticated API communication with backend endpoint

## Phase 3: User Story - Basic Chat Interface

### Goal
Enable users to navigate to `/chat` page and see the ChatKit UI with basic functionality.

### User Story
As a user, I want to visit `/chat` page and see the ChatKit UI so that I can start interacting with the todo management system via natural language.

### Independent Test Criteria
- User can navigate to `/chat` page
- ChatKit UI is rendered properly
- Basic chat functionality is available

### Implementation Tasks

- [ ] T005 [P] [US1] Replace /frontend/app/chat/page.tsx with proper ChatKit component implementation
- [ ] T006 [US1] Configure ChatKit with domain key from environment variables

## Phase 4: User Story - Message Sending with Authentication

### Goal
Enable users to send messages that are properly authenticated and processed by the backend.

### User Story
As a user, I want to send messages through the ChatKit interface that are authenticated with my user context so that my requests are properly associated with my account.

### Independent Test Criteria
- User session information (user_id and JWT) is retrieved
- Messages are sent to backend with proper authentication headers
- Backend receives authenticated requests with correct user context

### Implementation Tasks

- [ ] T007 [P] [US2] Implement onSendMessage handler in chat page using ChatKit's native handler
- [ ] T008 [US2] Integrate Better Auth session access in ChatKit component
- [ ] T009 [US2] Implement authenticated API call to POST /api/${user_id}/chat
- [ ] T010 [US2] Handle response from backend and return to ChatKit

## Phase 5: User Story - Conversation Persistence

### Goal
Enable users to maintain conversation context across page reloads using conversation_id.

### User Story
As a user, I want my conversation to persist when I reload the page so that I can continue my interaction without losing context.

### Independent Test Criteria
- Conversation ID is maintained and passed to backend
- Conversation history is restored on page load
- New conversations are created when no conversation ID exists

### Implementation Tasks

- [ ] T011 [P] [US3] Add conversation_id parameter handling in chat page
- [ ] T012 [US3] Implement conversation restoration logic on initial load
- [ ] T013 [US3] Pass conversation_id to ChatKit onSendMessage handler when available
- [ ] T014 [US3] Handle new conversation creation when no conversation_id is provided

## Phase 6: User Story - Error Handling

### Goal
Provide users with clear feedback when errors occur during chat interactions.

### User Story
As a user, I want to receive clear feedback when errors occur during chat interactions so that I understand what went wrong and how to proceed.

### Independent Test Criteria
- Invalid JWT tokens result in appropriate error messages
- Network failures during message sending are handled gracefully
- Invalid conversation IDs are handled properly

### Implementation Tasks

- [ ] T015 [P] [US4] Implement error handling for invalid JWT tokens in ChatKit component
- [ ] T016 [US4] Add network error handling for API communication
- [ ] T017 [US4] Handle invalid conversation ID scenarios gracefully

## Phase 7: Polish & Cross-Cutting Concerns

### Goal
Complete the implementation with documentation and deployment readiness.

### Independent Test Criteria
- README.md includes OpenAI domain allowlist instructions
- Deployment instructions are clear and actionable
- All acceptance criteria from spec are met

### Implementation Tasks

- [ ] T018 Update README.md with OpenAI ChatKit domain allowlist setup instructions
- [ ] T019 Verify all acceptance criteria from spec are implemented
- [ ] T020 Test end-to-end flow: "Add a task to buy eggs" → appears in DB
- [ ] T021 Test conversation persistence: page reload → conversation continues
- [ ] T022 Test error handling: invalid token → handled gracefully

## Dependencies

### User Story Completion Order
1. US1 (Basic Chat Interface) → Required by all other stories
2. US2 (Message Sending with Authentication) → Required by US3
3. US3 (Conversation Persistence) → Independent
4. US4 (Error Handling) → Independent

## Parallel Execution Examples

### Per User Story
- **US1**: T005 can be developed in parallel with T006
- **US2**: T007, T008, T009, T010 can be developed sequentially as they depend on each other
- **US3**: T011, T012, T013, T014 can be developed with some parallelization
- **US4**: T015, T016, T017 can be developed in parallel

## Implementation Strategy

### MVP Scope
- US1: Basic ChatKit UI rendering (T005-T006)
- US2: Basic authenticated message sending (T007-T010)

### Incremental Delivery
1. MVP: Basic chat interface with authentication
2. Add conversation persistence
3. Add error handling
4. Complete documentation and deployment readiness