// context/AuthContext.tsx
'use client';

import React, { createContext, useContext, useEffect, useState, ReactNode } from 'react';
import { User, Session, ApiResponse } from '@/types';
import authService from '@/services/authService';

interface AuthContextType {
  user: User | null;
  session: Session | null;
  loading: boolean;
  signIn: (email: string, password: string) => Promise<boolean>;
  signUp: (email: string, password: string) => Promise<boolean>; // Updated to remove name parameter
  signOut: () => Promise<void>;
  restoreSession: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

interface AuthProviderProps {
  children: ReactNode;
}

export const AuthProvider: React.FC<AuthProviderProps> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [session, setSession] = useState<Session | null>(null);
  const [loading, setLoading] = useState(true);

  // Sign in function using authService
  const signIn = async (email: string, password: string): Promise<boolean> => {
    const result: ApiResponse<{ user: User; session: Session }> = await authService.signIn(email, password);

    if (result.success && result.data) {
      setUser(result.data.user);
      setSession(result.data.session);

      // Store session in localStorage
      localStorage.setItem('session', JSON.stringify(result.data.session));
      localStorage.setItem('user', JSON.stringify(result.data.user));

      return true;
    } else {
      console.error('Sign in failed:', result.error?.message);
      return false;
    }
  };

  // Sign up function using authService - updated to match new signature
  const signUp = async (email: string, password: string): Promise<boolean> => {
    const result: ApiResponse<{ user: User; session: Session }> = await authService.signUp(email, password);

    if (result.success && result.data) {
      setUser(result.data.user);
      setSession(result.data.session);

      // Store session in localStorage
      localStorage.setItem('session', JSON.stringify(result.data.session));
      localStorage.setItem('user', JSON.stringify(result.data.user));

      return true;
    } else {
      console.error('Sign up failed:', result.error?.message);
      return false;
    }
  };

  // Sign out function using authService
  const signOut = async (): Promise<void> => {
    await authService.signOut();
    setUser(null);
    setSession(null);
    localStorage.removeItem('session');
    localStorage.removeItem('user');
  };

  // Restore session from localStorage
  const restoreSession = async (): Promise<void> => {
    try {
      // Try to get current user using the auth service
      const result: ApiResponse<User> = await authService.getCurrentUser();

      if (result.success && result.data) {
        // Get session data from localStorage if available
        const sessionData = localStorage.getItem('session');

        let sessionObj: Session | null = null;
        if (sessionData) {
          sessionObj = JSON.parse(sessionData);
        } else {
          // Create a basic session object if none exists
          sessionObj = {
            userId: result.data.id,
            token: localStorage.getItem('accessToken') || '',
            expiresAt: new Date(Date.now() + 24 * 60 * 60 * 1000), // 24 hours
            createdAt: new Date(),
          };

          // Store session in localStorage
          localStorage.setItem('session', JSON.stringify(sessionObj));
        }

        setUser(result.data);
        setSession(sessionObj);
      } else {
        // If not authenticated, clear any stored data
        localStorage.removeItem('session');
        localStorage.removeItem('user');
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
      }
    } catch (error) {
      console.error('Error restoring session:', error);
      localStorage.removeItem('session');
      localStorage.removeItem('user');
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    restoreSession();
  }, []);

  const value = {
    user,
    session,
    loading,
    signIn,
    signUp,
    signOut,
    restoreSession
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};