# Quickstart Guide: Frontend Interface (Standalone Prototype)

## Overview
This guide provides instructions for setting up and running the todo management frontend prototype with mock APIs and simulated authentication.

## Prerequisites
- Node.js 18.x or higher
- npm 8.x or higher (or yarn/bun)
- Git

## Getting Started

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <project-directory>
```

### 2. Install Dependencies
```bash
npm install
# or
yarn install
# or
bun install
```

### 3. Environment Configuration
Create a `.env.local` file in the project root with the following variables:

```env
# Mock API Configuration
NEXT_PUBLIC_API_MOCK_DELAY_MIN=500
NEXT_PUBLIC_API_MOCK_DELAY_MAX=1500

# Development settings
NEXT_PUBLIC_APP_ENV=development
NEXT_PUBLIC_BASE_URL=http://localhost:3000
```

### 4. Run Development Server
```bash
npm run dev
# or
yarn dev
# or
bun dev
```

The application will start on `http://localhost:3000`.

## Project Structure
```
frontend/
├── app/                    # Next.js App Router pages
│   ├── (auth)/            # Authentication routes
│   │   ├── sign-in/       # Sign in page
│   │   └── sign-up/       # Sign up page
│   ├── dashboard/         # Main dashboard
│   ├── todos/             # Todo management pages
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Home page
├── components/            # Reusable UI components
│   ├── ui/               # Base shadcn/ui components
│   └── forms/            # Form components
├── features/              # Feature-specific components
│   ├── auth/             # Authentication components
│   └── todos/            # Todo management components
├── services/              # API/service layer
│   ├── auth-service.ts   # Authentication API mock
│   └── todo-service.ts   # Todo API mock
├── hooks/                 # Custom React hooks
├── types/                 # TypeScript type definitions
├── lib/                   # Utility functions
└── public/                # Static assets
```

## Available Scripts

### Development
- `npm run dev` - Start development server with hot reloading
- `npm run lint` - Run ESLint to check for code issues
- `npm run type-check` - Run TypeScript type checking

### Production
- `npm run build` - Build the application for production
- `npm run start` - Start production server

### Testing
- `npm run test` - Run unit tests
- `npm run test:watch` - Run tests in watch mode

## Key Features

### Authentication Flow
1. Navigate to `/sign-up` to create an account
2. Use the sign-up form to register (mock data will be stored)
3. Navigate to `/sign-in` to log in with registered credentials
4. After successful authentication, you'll be redirected to the dashboard
5. Access protected routes (like `/todos`) while authenticated

### Todo Management
1. Create new todos using the add form
2. Edit existing todos by clicking the edit icon
3. Mark todos as complete/incomplete using the checkbox
4. Delete todos using the delete button
5. Filter todos by status or priority

## Mock API Behavior

### Authentication Mocks
- Sign-up: Creates a new user in mock storage
- Sign-in: Validates credentials against mock users
- Sign-out: Clears mock session data
- Session restoration: Checks localStorage on page load

### Todo Mocks
- Get todos: Returns mock todo data with configurable delays
- Create todo: Adds new todo to mock storage
- Update todo: Updates existing todo in mock storage
- Delete todo: Removes todo from mock storage
- Toggle completion: Updates completion status in mock storage

### Mock Delays
API calls include simulated network delays between 500-1500ms to mimic real-world conditions.

## Type Safety
The application uses TypeScript with strict type checking. All API responses and request bodies are typed according to the API contracts defined in `contracts/api-contracts.md`.

## Styling
- Tailwind CSS for utility-first styling
- shadcn/ui components for accessible UI elements
- Responsive design with mobile-first approach
- Dark mode support

## Testing

### Unit Tests
Run unit tests to verify individual components and services:
```bash
npm run test
```

### Integration Tests
Test complete user flows and API interactions:
```bash
npm run test:integration
```

## Deployment

### Building for Production
```bash
npm run build
```

### Running Production Build
```bash
npm run start
```

## Troubleshooting

### Common Issues

#### 1. Module Resolution Errors
If you encounter module resolution errors, try clearing the cache:
```bash
rm -rf node_modules package-lock.json
npm install
```

#### 2. Port Already in Use
If port 3000 is already in use, set a different port:
```bash
PORT=3001 npm run dev
```

#### 3. Environment Variables Not Loading
Ensure your `.env.local` file is in the correct location and restart the development server.

### Debugging Tips
- Check browser console for JavaScript errors
- Verify network requests in browser DevTools
- Use `console.log` statements for debugging (remove before committing)
- Enable React Developer Tools for component inspection

## Next Steps

### For Backend Integration
1. Replace mock API calls with real API endpoints
2. Implement JWT authentication
3. Connect to real database
4. Add server-side validation

### For Production Readiness
1. Add comprehensive error boundaries
2. Implement proper error logging
3. Add performance monitoring
4. Set up CI/CD pipeline