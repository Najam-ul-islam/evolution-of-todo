# Todo Application Frontend

A responsive Next.js frontend application for managing todos with authentication. This frontend connects to a real backend API with JWT-based authentication.

## Features

- **Authentication**: Secure login and signup functionality with JWT tokens
- **Todo Management**: Full CRUD operations for tasks with real API integration
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Dark Mode**: Automatic dark/light mode based on system preference
- **TypeScript**: Full type safety throughout the application
- **Shadcn/ui**: Consistent UI components

## Authentication

The application includes a complete authentication system:

- User registration and login via email/password
- JWT token-based authentication
- Protected routes that require authentication
- Secure token storage and management
- Session persistence across browser restarts

### Authentication Flow

1. Users register with email and password via `/sign-up`
2. Users login with email and password via `/sign-in`
3. JWT tokens are stored in localStorage upon successful login
4. Protected routes (like `/dashboard` and `/todos`) require valid authentication
5. Tokens are automatically included in API requests to protected endpoints

## Prerequisites

- Node.js (v18 or higher)
- npm or yarn

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd evolution-of-todo/frontend
```

2. Install dependencies:
```bash
npm install
```

## Configuration

Create a `.env.local` file in the frontend directory with the following variables:

```env
# Authentication Configuration
BETTER_AUTH_SECRET=your-better-auth-secret-change-in-production
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000

# Development settings
NEXT_PUBLIC_APP_ENV=development
NEXT_PUBLIC_BASE_URL=http://localhost:3000
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api

# Mock API Configuration (for development without backend)
NEXT_PUBLIC_API_MOCK_DELAY_MIN=500
NEXT_PUBLIC_API_MOCK_DELAY_MAX=1500
```

## Running the Application

1. Start the development server:
```bash
npm run dev
```

2. Open your browser and navigate to [http://localhost:3000](http://localhost:3000)

**Note**: Make sure the backend server is running on [http://localhost:8000](http://localhost:8000) for full functionality.

## Building for Production

To build the application for production:

```bash
npm run build
```

Then, to start the production server:

```bash
npm start
```

## Project Structure

```
frontend/
├── app/                           # Next.js 13+ App Router
│   ├── (auth)/                    # Authentication pages
│   │   ├── sign-in/page.tsx       # Sign in page
│   │   └── sign-up/page.tsx       # Sign up page
│   ├── dashboard/page.tsx         # Protected dashboard page
│   ├── todos/page.tsx             # Main todo management page
│   ├── layout.tsx                 # Root layout with AuthProvider
│   └── page.tsx                   # Landing page (redirects to auth/todos)
├── components/                    # Reusable components
│   ├── auth/                      # Authentication-specific components
│   │   ├── LoginForm.jsx          # Login form component
│   │   ├── SignupForm.jsx         # Signup form component
│   │   └── ProtectedRoute.jsx     # Route protection component
│   ├── features/todos/            # Todo-specific components
│   │   ├── TodoForm.tsx           # Todo creation/editing form
│   │   └── TodoItem.tsx           # Individual todo item component
│   ├── ui/                        # Shadcn/ui components
│   │   ├── button.tsx
│   │   └── input.tsx
│   │   └── ...
│   ├── ErrorBoundary.tsx          # Error boundary component
│   └── WithAuth.tsx               # Higher-order auth component
├── context/                       # React Context providers
│   └── AuthContext.tsx            # Authentication context
├── hooks/                         # Custom React hooks
│   └── useAuth.js                 # Authentication hook
├── lib/                           # Utility functions
│   ├── better-auth.js             # Better Auth configuration
│   ├── storage.ts                 # Local storage utilities
│   └── utils.ts                   # General utility functions
├── services/                      # API service functions
│   ├── api.ts                     # Base API service class
│   ├── authService.ts             # Authentication API functions
│   └── todoService.ts             # Todo API functions
├── types/                         # TypeScript type definitions
│   └── index.ts                   # Type interfaces
└── features/                      # Feature-specific code
```

## Authentication Components

The authentication system consists of several key components:

- `hooks/useAuth.js` - Custom hook for authentication state management
- `components/auth/` - Reusable authentication components
- `app/(auth)/` - Authentication pages (sign-in, sign-up)
- `app/dashboard/page.tsx` - Protected dashboard page
- `lib/better-auth.js` - Better Auth configuration

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## OpenAI ChatKit Setup

To use the AI-powered chatbot feature at `/chat`, you need to configure OpenAI ChatKit:

### 1. Register Domain in OpenAI Platform

1. Go to the [OpenAI Platform](https://platform.openai.com/) and sign in to your account
2. Navigate to the ChatKit section
3. Register your domains for both development and production:
   - For local development: Add `localhost` to the allowed domains
   - For production: Add your deployed domain (e.g., `your-app-name.vercel.app`)

### 2. Set NEXT_PUBLIC_OPENAI_DOMAIN_KEY in Vercel

1. In your Vercel project dashboard, go to Settings → Environment Variables
2. Add a new environment variable:
   - Key: `NEXT_PUBLIC_OPENAI_DOMAIN_KEY`
   - Value: The domain key provided by OpenAI after registering your domains

### 3. Local Development Setup

1. Copy the `.env.local.example` file to `.env.local`:
   ```bash
   cp .env.local.example .env.local
   ```
2. Update the `NEXT_PUBLIC_OPENAI_DOMAIN_KEY` value in `.env.local` with your OpenAI domain key

## License

This project is licensed under the MIT License.