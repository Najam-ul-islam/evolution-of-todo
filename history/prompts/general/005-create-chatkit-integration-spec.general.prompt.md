---
id: 005
title: Create Chatkit Integration Spec
stage: general
date: 2026-01-19
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: Claude
command: /sp.specify "OpenAI ChatKit Integration for AI-Powered Todo Chatbot"
labels: [spec, chatkit, integration, frontend]
links:
  spec: specs/001-chatkit-integration/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/001-chatkit-integration/spec.md
 - specs/001-chatkit-integration/checklists/requirements.md
tests:
 - none
---

## Prompt

/sp.specify

Feature: OpenAI ChatKit Integration for AI-Powered Todo Chatbot
@specs/features/chatkit.md

## Intent
Integrate the official **OpenAI ChatKit** as the frontend chat interface for Phase III of the Todo app, enabling natural-language task management via a polished, secure, and stateless UI.

## Context
- Project uses a **monorepo** with `/frontend` (Next.js 14 App Router) and `/backend` (FastAPI).
- Authentication is handled by **Better Auth** with JWT tokens.
- The backend exposes a **stateless chat endpoint**: `POST /api/{user_id}/chat`.
- This feature belongs to **Phase III** and must be implemented using **Spec-Driven Development** with **Claude Code** and **Spec-Kit Plus**.

## Requirements
1. **Install** `@openai/chatkit` in `/frontend` via npm.
2. **Create page** at `/frontend/app/chat/page.tsx` that renders `<ChatKit>`.
3. **Implement `onSendMessage`** handler that:
   - Fetches authenticated `user_id` from Better Auth session.
   - Sends `{ message, conversation_id? }` to `POST /api/${user_id}/chat`.
   - Includes `Authorization: Bearer <JWT>` header.
   - Returns `{ response, conversation_id }` to ChatKit.
4. **Configure domain key** via `NEXT_PUBLIC_OPENAI_DOMAIN_KEY` (from `.env.local`).
5. **Restore conversation history** when `conversation_id` is present.
6. **Add domain allowlist instructions** to `README.md` (for Vercel deployment).

## Acceptance Criteria
✅ User visits `/chat` → sees ChatKit UI
✅ Types "Add a task to call mom" → task appears in DB
✅ Page reload retains conversation via `conversation_id`
✅ All requests include valid JWT
✅ No custom chat components—only `@openai/chatkit` is used
✅ Works on `localhost` and `*.vercel.app` after domain allowlist

## Non-Goals
- Voice input
- Streaming responses
- Custom theming beyond ChatKit defaults
- Multi-user chat

## Dependencies
- @openai/chatkit ≥ 0.1.0
- Better Auth session available in Next.js client context
- Backend `/api/{user_id}/chat` already implemented (@specs/api/chat-endpoint.md)
- JWT token issued by Better Auth (@specs/features/authentication.md)

## Spec References
- UI structure: @specs/ui/pages.md
- Auth flow: @specs/features/authentication.md
- Chat API: @specs/api/chat-endpoint.md
- Phase III scope: @specs/overview.md#phase3-chatbot

## Deliverables
- `/frontend/app/chat/page.tsx`
- `/frontend/.env.local.example` (with `NEXT_PUBLIC_OPENAI_DOMAIN_KEY`)
- Updated `README.md` with OpenAI domain allowlist steps
- Entry in `@specs/ui/pages.md` listing `/chat` as a route

## Response snapshot

Created the specification for OpenAI ChatKit Integration feature with complete functional requirements, success criteria, user scenarios, and validation checklist.

## Outcome

- ✅ Impact: Successfully created comprehensive spec for ChatKit integration
- 🧪 Tests: none
- 📁 Files: Created specs/001-chatkit-integration/spec.md and requirements checklist
- 🔁 Next prompts: Ready for planning phase
- 🧠 Reflection: Spec covers all required functionality with clear acceptance criteria

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): All validation items passed
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A