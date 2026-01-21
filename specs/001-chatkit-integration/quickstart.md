# Quickstart: OpenAI ChatKit Integration for Todo Chatbot

## Prerequisites

- Node.js 18+ installed
- Existing Next.js 16 project with App Router in `/frontend` directory
- Better Auth configured for authentication
- Backend API with `/api/{user_id}/chat` endpoint
- OpenAI account with ChatKit access

## Setup Steps

### 1. Install Dependencies
```bash
cd frontend
npm install @openai/chatkit
```

### 2. Configure Environment Variables
Create or update `.env.local`:
```env
NEXT_PUBLIC_OPENAI_DOMAIN_KEY=your_openai_domain_key_here
```

### 3. Create Chat Page
Create `/frontend/app/chat/page.tsx` with ChatKit component and authentication integration.

### 4. Implement Authentication
- Use Better Auth session to get user_id and JWT token
- Include JWT token in API calls to backend
- Verify session validity before making requests

### 5. Connect to Backend API
- Implement onSendMessage handler
- Send authenticated requests to `/api/{user_id}/chat`
- Handle conversation persistence with conversation_id

## Development

### Running Locally
```bash
cd frontend
npm run dev
```

Visit http://localhost:3000/chat to access the chat interface.

### Testing
- Verify ChatKit UI renders properly
- Test authentication flow with Better Auth
- Confirm API communication with backend
- Validate conversation persistence

## Deployment

### Vercel Setup
1. Add domain to OpenAI ChatKit allowlist
2. Configure environment variables in Vercel dashboard
3. Deploy the application

### Domain Configuration
- For localhost development: Add `localhost` to domain allowlist
- For production: Add your Vercel domain (e.g., `your-project.vercel.app`)

## Troubleshooting

### Common Issues
- **Domain not allowed**: Ensure your domain is added to OpenAI ChatKit allowlist
- **Authentication errors**: Verify Better Auth is properly configured
- **API communication failures**: Check backend endpoint is accessible

### Debugging Tips
- Check browser console for JavaScript errors
- Verify environment variables are properly set
- Confirm backend API is returning expected responses