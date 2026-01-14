// app/todos/page.tsx
'use client';

import { useState, useEffect } from 'react';
import { useAuth } from '@/context/AuthContext';
import { useRouter } from 'next/navigation';
import TodoForm from '@/components/features/todos/TodoForm';
import TodoItem from '@/components/features/todos/TodoItem';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Badge } from '@/components/ui/badge';
import { Todo } from '@/types';
import todoService from '@/services/todoService';

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
      loadTodos();
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
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-gray-900"></div>
      </div>
    );
  }

  if (!user) {
    return null; // WithAuth will handle the redirect
  }

  const activeTodos = todos.filter(todo => !todo.completed);
  const completedTodos = todos.filter(todo => todo.completed);

  return (
    <div className="container mx-auto py-10">
      <div className="max-w-4xl mx-auto">
        <div className="flex justify-between items-center mb-8">
          <h1 className="text-3xl font-bold">My Todos</h1>
          <Button
            onClick={async () => {
              await signOut();
              router.push('/sign-in');
            }}
            variant="outline"
          >
            Sign Out
          </Button>
        </div>

        <Card className="mb-8">
          <CardHeader>
            <CardTitle>Create New Todo</CardTitle>
          </CardHeader>
          <CardContent>
            <TodoForm onSubmit={handleCreateTodo} />
          </CardContent>
        </Card>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded relative mb-4" role="alert">
            {error}
          </div>
        )}

        <Tabs defaultValue="active" className="w-full">
          <TabsList className="grid w-full grid-cols-2">
            <TabsTrigger value="active">
              Active ({activeTodos.length})
            </TabsTrigger>
            <TabsTrigger value="completed">
              Completed ({completedTodos.length})
            </TabsTrigger>
          </TabsList>
          <TabsContent value="active" className="mt-6">
            {loadingTodos ? (
              <div className="flex justify-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900"></div>
              </div>
            ) : activeTodos.length === 0 ? (
              <div className="text-center py-10">
                <p className="text-gray-500">No active todos. Great job!</p>
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
              <div className="flex justify-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900"></div>
              </div>
            ) : completedTodos.length === 0 ? (
              <div className="text-center py-10">
                <p className="text-gray-500">No completed todos yet.</p>
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
  );
}