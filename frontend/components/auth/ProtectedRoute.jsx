'use client';

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/hooks/useAuth';

const ProtectedRoute = ({ children }) => {
  const router = useRouter();
  const { user, loading } = useAuth();
  const [authorized, setAuthorized] = useState(false);

  useEffect(() => {
    // Check if user is authenticated
    if (!loading) {
      if (!user) {
        // Redirect to sign in page if not authenticated
        router.push('/signin');
      } else {
        setAuthorized(true);
      }
    }
  }, [user, loading, router]);

  // Show loading while checking authentication status
  if (loading || !authorized) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  // Render children only if user is authorized
  return <>{children}</>;
};

export default ProtectedRoute;