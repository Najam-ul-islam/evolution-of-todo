import { createAuthClient } from 'better-auth/react';

// Initialize real client only on browser
// On the server, we'll use a placeholder that won't be used during rendering
let client;

if (typeof window !== 'undefined') {
  // Client-side: Initialize the real auth client
  client = createAuthClient({
    baseURL: process.env.NEXT_PUBLIC_BETTER_AUTH_URL || 'http://localhost:8000/api/auth', // Adjust based on your backend URL
    fetchOptions: {
      // Additional fetch options if needed
    }
  });
} else {
  // Server-side: Create a placeholder client with a minimal store structure
  // This is only to prevent errors during SSR, the real client will be initialized on the client
  const createMinimalStore = () => {
    const listeners = [];

    return {
      get: () => ({ data: null, isLoading: true }),
      subscribe: (callback) => {
        listeners.push(callback);
        return () => {
          const index = listeners.indexOf(callback);
          if (index > -1) {
            listeners.splice(index, 1);
          }
        };
      },
      notify: () => {
        listeners.forEach(cb => cb());
      },
      listen: (signal, callback) => {
        // Placeholder implementation
        return () => {};
      },
      atoms: {}
    };
  };

  client = {
    sessionStore: createMinimalStore() // Changed from $store to sessionStore
  };
}

export const authClient = client;