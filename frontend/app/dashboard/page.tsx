"use client";

import { useRouter } from "next/navigation";
import { useAuth } from "@/context/AuthContext";
import { Button } from "@/components/ui/button";
import { LogOut, User, CheckSquare, BarChart3 } from "lucide-react"; // ✅ Fixed import
import FloatingChat from "@/components/FloatingChat";

export default function DashboardPage() {
  const router = useRouter();
  const { user, signOut } = useAuth();

  const handleLogout = async () => {
    await signOut();
    router.push("/sign-in");
  };

  return (
    <>
      <div className="min-h-screen bg-gradient-to-br from-primary/5 to-secondary">
        <div className="container mx-auto px-4 py-8 max-w-6xl">
          <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
            <div>
              <h1 className="text-4xl font-bold bg-gradient-to-r from-primary to-indigo-600 bg-clip-text text-transparent">
                Dashboard
              </h1>
              <p className="text-muted-foreground mt-2">
                Welcome to your personalized workspace
              </p>
            </div>

            <Button
              onClick={handleLogout}
              variant="outline"
              className="gap-2 border-2 hover:bg-destructive hover:text-destructive-foreground"
            >
              <LogOut className="h-4 w-4" />
              Sign Out
            </Button>
          </div>

          <div className="mb-10">
            <h2 className="text-2xl font-bold text-foreground mb-2">
              Welcome back, {user?.email}!
            </h2>
            <p className="text-muted-foreground">
              You are successfully logged in. This is a protected dashboard page
              that can only be accessed by authenticated users.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
            <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl p-6 text-white card-elevated">
              <div className="flex items-center gap-3 mb-3">
                <User className="h-8 w-8" />
                <h3 className="text-xl font-bold">Account</h3>
              </div>
              <p className="opacity-90">Manage your profile and preferences</p>
              <Button className="mt-4 bg-white text-blue-600 hover:bg-blue-50">
                Manage Account
              </Button>
            </div>

            <div className="bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl p-6 text-white card-elevated">
              <div className="flex items-center gap-3 mb-3">
                <CheckSquare className="h-8 w-8" />
                <h3 className="text-xl font-bold">Tasks</h3>
              </div>
              <p className="opacity-90">View and manage your todo list</p>
              <Button
                onClick={() => router.push("/todos")}
                className="mt-4 bg-white text-indigo-600 hover:bg-indigo-50"
              >
                View Tasks
              </Button>
            </div>

            <div className="bg-gradient-to-br from-emerald-500 to-teal-600 rounded-xl p-6 text-white card-elevated">
              <div className="flex items-center gap-3 mb-3">
                <BarChart3 className="h-8 w-8" />
                <h3 className="text-xl font-bold">Analytics</h3>
              </div>
              <p className="opacity-90">Track your productivity and progress</p>
              <Button className="mt-4 bg-white text-emerald-600 hover:bg-emerald-50">
                View Analytics
              </Button>
            </div>

            <div className="bg-gradient-to-br from-orange-500 to-red-600 rounded-xl p-6 text-white card-elevated">
              <div className="flex items-center gap-3 mb-3">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="h-8 w-8"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  strokeWidth="2"
                >
                  <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
                </svg>
                <h3 className="text-xl font-bold">Chat</h3>
              </div>
              <p className="opacity-90">Chat with our AI assistant</p>
              <Button
                onClick={() => router.push("/chat")}
                className="mt-4 bg-white text-orange-600 hover:bg-orange-50"
              >
                Open Chat
              </Button>
            </div>
          </div>

          <div className="bg-card rounded-xl p-8 border border-border card-elevated">
            <h3 className="text-2xl font-bold text-foreground mb-4">
              Quick Actions
            </h3>
            <div className="flex flex-wrap gap-4">
              <Button
                onClick={() => router.push("/todos")}
                className="bg-gradient-to-r from-primary to-indigo-600 hover:from-primary/90 hover:to-indigo-700 text-primary-foreground"
              >
                Go to Todo List
              </Button>
              <Button variant="outline" className="border-2">
                View Profile
              </Button>
              <Button variant="outline" className="border-2">
                Settings
              </Button>
            </div>
          </div>
        </div>
      </div>

      <FloatingChat />
    </>
  );
}
