---
id: "010"
title: "Fix Better Auth Session Hook Usage"
stage: "refactor"
date: "2026-01-21"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "001-chatkit-integration"
user: "user"
command: "fix better auth session hook usage"
labels: ["authentication", "better-auth", "typescript", "refactor"]
spec: null
ticket: null
pr: null
adr: null
---

# Fix Better Auth Session Hook Usage

## Summary

Fixed authentication implementation in FloatingChatWidget component by updating from the deprecated `useSession()` hook to the correct `useStore(authClient.sessionStore)` approach for the current version of Better Auth.

## Changes Made

### Files Modified

- `frontend/components/FloatingChatWidget.tsx`: Updated authentication hook usage

### Technical Details

**Before:**
```tsx
// ❌ Wrong approach for current Better Auth version
const { data: session, isLoading } = useSession();

// Conditional rendering
if (isLoading || !session) return null;
```

**After:**
```tsx
// ✅ Correct approach for current Better Auth version
const store = useStore(authClient.sessionStore);
const session = store?.data;
const isLoading = store?.isLoading ?? true;

// Conditional rendering
if (isLoading) return null;
if (!session?.user) return null;
```

## Problem Solved

- Fixed "Export 'useSession' doesn't exist in target module" error
- Properly integrated with Better Auth's session store mechanism
- Eliminated incorrect typing overrides that were causing runtime crashes
- Ensured proper hydration-safe authentication state management

## Testing

- Development server runs successfully on port 3001
- Authentication flow properly handles loading states
- Session data is correctly accessed via the store pattern
- Both chat page and floating widget now use consistent authentication approach

## Outcome

The authentication system now works properly with the current version of Better Auth, eliminating the runtime crashes and TypeScript errors that were occurring with the incorrect `useSession()` hook usage.