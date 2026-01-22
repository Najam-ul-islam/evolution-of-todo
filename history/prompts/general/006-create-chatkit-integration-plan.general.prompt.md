---
id: 006
title: Create Chatkit Integration Plan
stage: general
date: 2026-01-19
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 001-chatkit-integration
user: Claude
command: /sp.plan "OpenAI ChatKit Integration for Todo Chatbot"
labels: [plan, chatkit, integration, frontend]
links:
  spec: specs/001-chatkit-integration/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/001-chatkit-integration/plan.md
 - specs/001-chatkit-integration/research.md
 - specs/001-chatkit-integration/data-model.md
 - specs/001-chatkit-integration/quickstart.md
 - specs/001-chatkit-integration/contracts/api.md
tests:
 - none
---

## Prompt

/sp.plan

Plan: Implement OpenAI ChatKit Integration for Todo Chatbot
Based on: @specs/features/chatkit.md

Objective:
Generate a complete, secure, and spec-compliant frontend integration of OpenAI ChatKit in the Next.js app, connecting to the existing FastAPI chat endpoint with proper authentication and conversation persistence.

Scope:
- Frontend only (`/frontend`)
- Uses existing backend (`/api/{user_id}/chat`)
- Leverages Better Auth session for user context
- No changes to backend or database

Key Milestones:
1. Environment & dependency setup
2. Auth-aware chat page creation
3. ChatKit ↔ FastAPI integration
4. Domain key configuration & testing
5. Documentation & deployment readiness

Constraints:
- Must use `@openai/chatkit` (no custom UI)
- Must not hardcode user_id or tokens
- Must work in development and production (Vercel)
- All code generated via Claude Code from specs

Deliverables:
- Working `/chat` page in Next.js App Router
- Secure API communication with JWT
- README updates for OpenAI domain allowlist
- Zero manual implementation

## Response snapshot

Created comprehensive implementation plan for OpenAI ChatKit Integration feature with complete research, data model, quickstart guide, and API contracts.

## Outcome

- ✅ Impact: Successfully created detailed plan for ChatKit integration with all required artifacts
- 🧪 Tests: none
- 📁 Files: Created plan.md, research.md, data-model.md, quickstart.md, and contracts/api.md
- 🔁 Next prompts: Ready for task generation phase
- 🧠 Reflection: Plan covers all aspects from architecture to implementation with proper security considerations

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): All planning artifacts created successfully
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A