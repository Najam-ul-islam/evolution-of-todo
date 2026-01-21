// app/todos/page.tsx
'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '@/context/AuthContext';
import { useRouter } from 'next/navigation';
import TodoForm from '@/components/features/todos/TodoForm';
import TodoItem from '@/components/features/todos/TodoItem';
import { Button } from '@/components/ui/button';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Todo } from '@/types';
import todoService from '@/services/todoService';
import LogOut from 'lucide-react/dist/esm/icons/log-out';
import CheckCircle from 'lucide-react/dist/esm/icons/check-circle';
import Circle from 'lucide-react/dist/esm/icons/circle';
import Calendar from 'lucide-react/dist/esm/icons/calendar';
import TrendingUp from 'lucide-react/dist/esm/icons/trending-up';
import Plus from 'lucide-react/dist/esm/icons/plus';

export default function TodosPage() {
  const { user, loading, signOut } = useAuth();
  const router = useRouter();
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loadingTodos, setLoadingTodos] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!loading && !user) {
      router.push('/sign-in');
    } else if (user) {
      const fetchTodos = async () => {
        await loadTodos();
      };
      fetchTodos();
    }
  }, [user, loading, router]);

  const loadTodos = async () => {
    if (!user) return;

    try {
      setLoadingTodos(true);
      const result = await todoService.getTodos(user.id);

      if (result.success) {
        setTodos(result.data || []);
      } else {
        setError(result.error?.message || 'Failed to load todos');
      }
    } catch (err) {
      setError('An unexpected error occurred');
      console.error('Error loading todos:', err);
    } finally {
      setLoadingTodos(false);
    }
  };

  const handleCreateTodo = async (title: string, description?: string, priority?: 'low' | 'medium' | 'high', dueDate?: Date | null) => {
    if (!user) return;

    try {
      const result = await todoService.createTodo(user.id, title, description, priority, dueDate);

      if (result.success && result.data) {
        setTodos([...todos, result.data]);
      } else {
        setError(result.error?.message || 'Failed to create todo');
      }
    } catch (err) {
      setError('An unexpected error occurred');
      console.error('Error creating todo:', err);
    }
  };

  const handleUpdateTodo = async (id: string, updates: Partial<Todo>) => {
    try {
      const result = await todoService.updateTodo(id, updates);

      if (result.success && result.data) {
        setTodos(todos.map(todo =>
          todo.id === id ? result.data! : todo
        ));
      } else {
        setError(result.error?.message || 'Failed to update todo');
      }
    } catch (err) {
      setError('An unexpected error occurred');
      console.error('Error updating todo:', err);
    }
  };

  const handleDeleteTodo = async (id: string) => {
    try {
      const result = await todoService.deleteTodo(id);

      if (result.success) {
        setTodos(todos.filter(todo => todo.id !== id));
      } else {
        setError(result.error?.message || 'Failed to delete todo');
      }
    } catch (err) {
      setError('An unexpected error occurred');
      console.error('Error deleting todo:', err);
    }
  };

  const handleToggleCompletion = async (id: string) => {
    try {
      const result = await todoService.toggleTodoCompletion(id);

      if (result.success && result.data) {
        setTodos(todos.map(todo =>
          todo.id === id ? { ...todo, completed: result.data!.completed } : todo
        ));
      } else {
        setError(result.error?.message || 'Failed to toggle completion');
      }
    } catch (err) {
      setError('An unexpected error occurred');
      console.error('Error toggling completion:', err);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary/5 to-secondary">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-primary mx-auto"></div>
          <p className="mt-4 text-lg text-muted-foreground">Loading your tasks...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return null; // WithAuth will handle the redirect
  }

  const activeTodos = todos.filter(todo => !todo.completed);
  const completedTodos = todos.filter(todo => todo.completed);

  // Calculate statistics
  const totalTodos = todos.length;
  const completedCount = completedTodos.length;
  const activeCount = activeTodos.length;
  const completionRate = totalTodos > 0 ? Math.round((completedCount / totalTodos) * 100) : 0;

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary/5 to-secondary">
      <div className="container mx-auto px-4 py-8 max-w-6xl">
        {/* Header */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
          <div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-primary to-indigo-600 bg-clip-text text-transparent">
              My Todo List
            </h1>
            <p className="text-muted-foreground mt-2">Organize your tasks and boost productivity</p>
          </div>

          <div className="flex items-center gap-3">
            <div className="hidden md:flex items-center gap-4 text-sm text-muted-foreground">
              <div className="flex items-center gap-1">
                <Circle className="h-4 w-4 text-blue-500" />
                <span>{activeCount} Active</span>
              </div>
              <div className="flex items-center gap-1">
                <CheckCircle className="h-4 w-4 text-green-500" />
                <span>{completedCount} Completed</span>
              </div>
              <div className="flex items-center gap-1">
                <TrendingUp className="h-4 w-4 text-purple-500" />
                <span>{completionRate}% Complete</span>
              </div>
            </div>

            <Button
              onClick={() => router.push('/dashboard')}
              variant="outline"
              className="gap-2 border-2"
            >
              <TrendingUp className="h-4 w-4" />
              Dashboard
            </Button>

            <Button
              onClick={async () => {
                await signOut();
                router.push('/sign-in');
              }}
              variant="outline"
              className="gap-2 border-2 hover:bg-destructive hover:text-destructive-foreground"
            >
              <LogOut className="h-4 w-4" />
              Sign Out
            </Button>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl p-5 text-white card-elevated">
            <div className="text-3xl font-bold">{totalTodos}</div>
            <div className="text-sm opacity-90">Total Tasks</div>
          </div>
          <div className="bg-gradient-to-br from-indigo-500 to-indigo-600 rounded-xl p-5 text-white card-elevated">
            <div className="text-3xl font-bold">{activeCount}</div>
            <div className="text-sm opacity-90">Active</div>
          </div>
          <div className="bg-gradient-to-br from-green-500 to-emerald-600 rounded-xl p-5 text-white card-elevated">
            <div className="text-3xl font-bold">{completedCount}</div>
            <div className="text-sm opacity-90">Completed</div>
          </div>
          <div className="bg-gradient-to-br from-purple-500 to-violet-600 rounded-xl p-5 text-white card-elevated">
            <div className="text-3xl font-bold">{completionRate}%</div>
            <div className="text-sm opacity-90">Progress</div>
          </div>
        </div>

        {/* Create Todo Form */}
        <div className="mb-8">
          <div className="flex items-center gap-2 mb-4">
            <Plus className="h-5 w-5 text-primary" />
            <h2 className="text-2xl font-bold text-foreground">Create New Task</h2>
          </div>
          <TodoForm onSubmit={handleCreateTodo} />
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-destructive/10 border border-destructive text-destructive px-4 py-3 rounded-lg mb-6 flex items-center gap-2" role="alert">
            <span>Error:</span>
            <span>{error}</span>
          </div>
        )}

        {/* Tabs for Active/Completed */}
        <div className="bg-card rounded-xl p-1 border border-border card-elevated">
          <Tabs defaultValue="active" className="w-full">
            <TabsList className="grid w-full grid-cols-2 bg-muted rounded-lg p-1">
              <TabsTrigger
                value="active"
                className="relative rounded-md data-[state=active]:shadow-sm data-[state=active]:bg-background data-[state=active]:text-foreground"
              >
                <div className="flex items-center gap-2">
                  <Circle className="h-4 w-4" />
                  Active ({activeCount})
                </div>
              </TabsTrigger>
              <TabsTrigger
                value="completed"
                className="relative rounded-md data-[state=active]:shadow-sm data-[state=active]:bg-background data-[state=active]:text-foreground"
              >
                <div className="flex items-center gap-2">
                  <CheckCircle className="h-4 w-4" />
                  Completed ({completedCount})
                </div>
              </TabsTrigger>
            </TabsList>
            <TabsContent value="active" className="mt-6">
              {loadingTodos ? (
                <div className="flex justify-center py-10">
                  <div className="animate-spin rounded-full h-12 w-12 border-t-4 border-primary"></div>
                </div>
              ) : activeTodos.length === 0 ? (
                <div className="text-center py-16">
                  <div className="mx-auto w-24 h-24 bg-muted rounded-full flex items-center justify-center mb-4">
                    <CheckCircle className="h-12 w-12 text-muted-foreground" />
                  </div>
                  <h3 className="text-xl font-semibold text-foreground mb-2">No active tasks</h3>
                  <p className="text-muted-foreground max-w-md mx-auto">
                    Great job! You've completed all your tasks. Add a new task to get started.
                  </p>
                </div>
              ) : (
                <div className="space-y-4">
                  {activeTodos.map(todo => (
                    <TodoItem
                      key={todo.id}
                      todo={todo}
                      onUpdate={handleUpdateTodo}
                      onDelete={handleDeleteTodo}
                      onToggleCompletion={handleToggleCompletion}
                    />
                  ))}
                </div>
              )}
            </TabsContent>
            <TabsContent value="completed" className="mt-6">
              {loadingTodos ? (
                <div className="flex justify-center py-10">
                  <div className="animate-spin rounded-full h-12 w-12 border-t-4 border-primary"></div>
                </div>
              ) : completedTodos.length === 0 ? (
                <div className="text-center py-16">
                  <div className="mx-auto w-24 h-24 bg-muted rounded-full flex items-center justify-center mb-4">
                    <Calendar className="h-12 w-12 text-muted-foreground" />
                  </div>
                  <h3 className="text-xl font-semibold text-foreground mb-2">No completed tasks yet</h3>
                  <p className="text-muted-foreground max-w-md mx-auto">
                    Start completing your tasks to see them appear here. You got this!
                  </p>
                </div>
              ) : (
                <div className="space-y-4">
                  {completedTodos.map(todo => (
                    <TodoItem
                      key={todo.id}
                      todo={todo}
                      onUpdate={handleUpdateTodo}
                      onDelete={handleDeleteTodo}
                      onToggleCompletion={handleToggleCompletion}
                    />
                  ))}
                </div>
              )}
            </TabsContent>
          </Tabs>
        </div>
      </div>
    </div>
  );
}