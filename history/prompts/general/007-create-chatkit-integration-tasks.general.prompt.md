---
id: 007
title: Create Chatkit Integration Tasks
stage: general
date: 2026-01-19
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 001-chatkit-integration
user: Claude
command: /sp.tasks "OpenAI ChatKit Integration for Todo Chatbot"
labels: [tasks, chatkit, integration, frontend]
links:
  spec: specs/001-chatkit-integration/spec.md
  plan: specs/001-chatkit-integration/plan.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/001-chatkit-integration/tasks.md
tests:
 - none
---

## Prompt

/sp.tasks

Break down the implementation of @specs/features/chatkit.md into discrete, Claude Code–executable tasks.

Each task must:
- Be implementable by a single Claude Code generation step
- Reference relevant spec sections
- Output files in correct monorepo paths
- Assume no prior manual code exists

Tasks:

1. **Install ChatKit dependency**
   - Run: `npm install @openai/chatkit` in `/frontend`
   - Update `package.json` and `package-lock.json`
   - Reference: @specs/features/chatkit.md#Requirements.1

2. **Create chat page route**
   - Generate `/frontend/app/chat/page.tsx`
   - Import `ChatKit` and CSS from `@openai/chatkit`
   - Render basic `<ChatKit />` with placeholder config
   - Reference: @specs/features/chatkit.md#Requirements.2

3. **Implement Better Auth session integration**
   - Create `/frontend/lib/auth.ts` to extract `user_id` and `jwt` from session
   - Use `getServerSession()` or client-side auth hook as appropriate
   - Reference: @specs/features/chatkit.md#Requirements.3 + @specs/features/authentication.md

4. **Build onSendMessage handler**
   - In `page.tsx`, define async `handleSend(message, conversationId?)`
   - Fetch user session → get `user_id` and `token`
   - POST to `/api/${user_id}/chat` with headers and body
   - Return `{ response, conversation_id }`
   - Reference: @specs/features/chatkit.md#Requirements.3

5. **Configure ChatKit with domain key**
   - Add `NEXT_PUBLIC_OPENAI_DOMAIN_KEY` to `.env.local.example`
   - Load key in `page.tsx` and pass to `<ChatKit domainKey={...} />`
   - Reference: @specs/features/chatkit.md#Requirements.4

6. **Add conversation history support**
   - On initial load, check URL or local state for `conversation_id`
   - Pass it to `onSendMessage` on first message if available
   - Ensure backend can resume via `conversation_id`
   - Reference: @specs/features/chatkit.md#Requirements.5

7. **Update README with deployment instructions**
   - Add section: “OpenAI ChatKit Setup”
   - Include steps to:
     a. Register domain in OpenAI Platform
     b. Set `NEXT_PUBLIC_OPENAI_DOMAIN_KEY` in Vercel
   - Reference: @specs/features/chatkit.md#Requirements.6

8. **Verify end-to-end flow**
   - Test: “Add a task to buy eggs” → appears in DB
   - Test: Reload → conversation continues
   - Test: Invalid token → handled gracefully
   - Reference: @specs/features/chatkit.md#Acceptance Criteria

## Response snapshot

Created comprehensive tasks.md file with 22 specific tasks organized into 7 phases for implementing the ChatKit integration according to the specification and plan.

## Outcome

- ✅ Impact: Successfully created detailed task breakdown for ChatKit integration
- 🧪 Tests: none
- 📁 Files: Created specs/001-chatkit-integration/tasks.md with complete task breakdown
- 🔁 Next prompts: Ready for implementation phase
- 🧠 Reflection: Tasks are organized by user stories and phases for incremental delivery

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): All tasks follow required format and reference spec sections
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A