// app/dashboard/page.tsx
'use client';

import { useRouter } from 'next/navigation';
import { useAuth } from '@/hooks/useAuth';
import ProtectedRoute from '@/components/auth/ProtectedRoute';
import { Button } from '@/components/ui/button';

export default function DashboardPage() {
  const router = useRouter();
  const { user, logout } = useAuth();

  const handleLogout = async () => {
    await logout();
    router.push('/signin');
  };

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
        <div className="max-w-3xl mx-auto">
          <div className="bg-white p-8 rounded-lg shadow-md">
            <div className="flex justify-between items-center mb-6">
              <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
              <Button
                onClick={handleLogout}
                className="bg-red-500 hover:bg-red-600 text-white"
              >
                Logout
              </Button>
            </div>

            <div className="mb-8">
              <h2 className="text-xl font-semibold text-gray-800 mb-4">Welcome, {user?.email}!</h2>
              <p className="text-gray-600">
                You are successfully logged in. This is a protected dashboard page that can only be accessed by authenticated users.
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              <div className="bg-blue-50 p-6 rounded-lg border border-blue-100">
                <h3 className="text-lg font-medium text-blue-800 mb-2">Your Account</h3>
                <p className="text-gray-600">Manage your account settings and profile information.</p>
              </div>

              <div className="bg-green-50 p-6 rounded-lg border border-green-100">
                <h3 className="text-lg font-medium text-green-800 mb-2">Your Tasks</h3>
                <p className="text-gray-600">View and manage your todo tasks.</p>
              </div>
            </div>

            <div className="mt-8">
              <Button
                onClick={() => router.push('/todos')}
                className="bg-indigo-600 hover:bg-indigo-700 text-white"
              >
                Go to Todo List
              </Button>
            </div>
          </div>
        </div>
      </div>
    </ProtectedRoute>
  );
}