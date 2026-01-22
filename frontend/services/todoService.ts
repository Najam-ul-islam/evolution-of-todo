// services/todoService.ts
import ApiService, { delay } from './api';
import { Todo, ApiResponse } from '@/types';

class TodoService extends ApiService {
  private todos: Todo[] = [];

  constructor() {
    super();
    // Initialize with some mock todos for demonstration
    this.todos = [
      {
        id: 'todo_1',
        title: 'Sample Todo',
        description: 'This is a sample todo item',
        completed: false,
        priority: 'medium',
        dueDate: null,
        createdAt: new Date(),
        updatedAt: new Date(),
        userId: 'mock_user_123'
      },
      {
        id: 'todo_2',
        title: 'Another Sample Todo',
        description: 'This is another sample todo item',
        completed: true,
        priority: 'high',
        dueDate: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000), // 7 days from now
        createdAt: new Date(Date.now() - 24 * 60 * 60 * 1000), // 1 day ago
        updatedAt: new Date(Date.now() - 24 * 60 * 60 * 1000), // 1 day ago
        userId: 'mock_user_123'
      }
    ];
  }

  // TODO: Replace with real API call when connecting to backend
  // Include JWT token in Authorization header
  // SECURITY TODO: Validate that the requesting user can only access their own todos
  async getTodos(userId: string, filters?: { completed?: boolean; priority?: 'low' | 'medium' | 'high' }): Promise<ApiResponse<Todo[]>> {
    let filteredTodos = [...this.todos];

    // Apply filters
    if (filters?.completed !== undefined) {
      filteredTodos = filteredTodos.filter(todo => todo.completed === filters.completed);
    }

    if (filters?.priority) {
      filteredTodos = filteredTodos.filter(todo => todo.priority === filters.priority);
    }

    // Filter by user
    filteredTodos = filteredTodos.filter(todo => todo.userId === userId);

    return this.mockApiCall(filteredTodos);
  }

  // TODO: Replace with real API call when connecting to backend
  // Include JWT token in Authorization header
  // SECURITY TODO: Validate that the requesting user can only create todos for themselves
  // SECURITY TODO: Implement proper input sanitization to prevent XSS
  async createTodo(userId: string, title: string, description?: string, priority: 'low' | 'medium' | 'high' = 'medium', dueDate?: Date | null): Promise<ApiResponse<Todo>> {
    // Validation
    if (!title || title.trim().length === 0) {
      return {
        success: false,
        error: {
          message: 'Title is required',
          code: 'MISSING_REQUIRED_FIELD'
        }
      };
    }

    if (title.length > 255) {
      return {
        success: false,
        error: {
          message: 'Title must be less than 255 characters',
          code: 'VALUE_TOO_LONG'
        }
      };
    }

    if (description && description.length > 1000) {
      return {
        success: false,
        error: {
          message: 'Description must be less than 1000 characters',
          code: 'VALUE_TOO_LONG'
        }
      };
    }

    const newTodo: Todo = {
      id: `todo_${Date.now()}`,
      title: title.trim(),
      description: description || '',
      completed: false,
      priority,
      dueDate: dueDate || null,
      createdAt: new Date(),
      updatedAt: new Date(),
      userId
    };

    // Optimistic update: add the todo immediately
    const todoIndex = this.todos.length;
    this.todos.push(newTodo);

    try {
      // Simulate API call delay
      await delay(this.mockDelayMin, this.mockDelayMax);

      // Return the new todo
      return {
        success: true,
        data: newTodo
      };
    } catch (error) {
      // If there was an error, remove the optimistic update
      this.todos.splice(todoIndex, 1);
      return {
        success: false,
        error: {
          message: 'Failed to create todo',
          code: 'CREATE_ERROR'
        }
      };
    }
  }

  // TODO: Replace with real API call when connecting to backend
  // Include JWT token in Authorization header
  // SECURITY TODO: Validate that the requesting user owns the todo they're updating
  // SECURITY TODO: Implement proper input sanitization to prevent XSS
  async updateTodo(todoId: string, updates: Partial<Todo>): Promise<ApiResponse<Todo>> {
    const todoIndex = this.todos.findIndex(todo => todo.id === todoId);

    if (todoIndex === -1) {
      return {
        success: false,
        error: {
          message: 'Todo not found',
          code: 'TODO_NOT_FOUND'
        }
      };
    }

    // Validation for title if being updated
    if (updates.title !== undefined) {
      if (!updates.title || updates.title.trim().length === 0) {
        return {
          success: false,
          error: {
            message: 'Title is required',
            code: 'MISSING_REQUIRED_FIELD'
          }
        };
      }

      if (updates.title.length > 255) {
        return {
          success: false,
          error: {
            message: 'Title must be less than 255 characters',
            code: 'VALUE_TOO_LONG'
          }
        };
      }
    }

    // Validation for description if being updated
    if (updates.description !== undefined && updates.description.length > 1000) {
      return {
        success: false,
        error: {
          message: 'Description must be less than 1000 characters',
          code: 'VALUE_TOO_LONG'
        }
      };
    }

    // Optimistic update: update the todo immediately
    const previousTodo = { ...this.todos[todoIndex] };
    this.todos[todoIndex] = {
      ...this.todos[todoIndex],
      ...updates,
      updatedAt: new Date()
    };

    try {
      // Simulate API call delay
      await delay(this.mockDelayMin, this.mockDelayMax);

      // Return the updated todo
      return {
        success: true,
        data: this.todos[todoIndex]
      };
    } catch (error) {
      // If there was an error, revert the optimistic update
      this.todos[todoIndex] = previousTodo;
      return {
        success: false,
        error: {
          message: 'Failed to update todo',
          code: 'UPDATE_ERROR'
        }
      };
    }
  }

  // TODO: Replace with real API call when connecting to backend
  // Include JWT token in Authorization header
  // SECURITY TODO: Validate that the requesting user owns the todo they're deleting
  async deleteTodo(todoId: string): Promise<ApiResponse<{ message: string }>> {
    const todoIndex = this.todos.findIndex(todo => todo.id === todoId);

    if (todoIndex === -1) {
      return {
        success: false,
        error: {
          message: 'Todo not found',
          code: 'TODO_NOT_FOUND'
        }
      };
    }

    // Optimistic update: remove the todo immediately
    const deletedTodo = this.todos[todoIndex];
    this.todos.splice(todoIndex, 1);

    try {
      // Simulate API call delay
      await delay(this.mockDelayMin, this.mockDelayMax);

      // Return success
      return {
        success: true,
        data: { message: 'Todo deleted successfully' }
      };
    } catch (error) {
      // If there was an error, restore the deleted todo
      this.todos.splice(todoIndex, 0, deletedTodo);
      return {
        success: false,
        error: {
          message: 'Failed to delete todo',
          code: 'DELETE_ERROR'
        }
      };
    }
  }

  // TODO: Replace with real API call when connecting to backend
  // Include JWT token in Authorization header
  // SECURITY TODO: Validate that the requesting user owns the todo they're toggling
  async toggleTodoCompletion(todoId: string): Promise<ApiResponse<{ id: string; completed: boolean }>> {
    const todoIndex = this.todos.findIndex(todo => todo.id === todoId);

    if (todoIndex === -1) {
      return {
        success: false,
        error: {
          message: 'Todo not found',
          code: 'TODO_NOT_FOUND'
        }
      };
    }

    // Optimistic update: toggle the completion status immediately
    const previousCompleted = this.todos[todoIndex].completed;
    this.todos[todoIndex] = {
      ...this.todos[todoIndex],
      completed: !previousCompleted,
      updatedAt: new Date()
    };

    try {
      // Simulate API call delay
      await delay(this.mockDelayMin, this.mockDelayMax);

      // Return the updated status
      return {
        success: true,
        data: {
          id: todoId,
          completed: !previousCompleted
        }
      };
    } catch (error) {
      // If there was an error, revert the optimistic update
      this.todos[todoIndex] = {
        ...this.todos[todoIndex],
        completed: previousCompleted
      };
      return {
        success: false,
        error: {
          message: 'Failed to toggle completion',
          code: 'TOGGLE_ERROR'
        }
      };
    }
  }
}

export default new TodoService();