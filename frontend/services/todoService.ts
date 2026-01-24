// services/todoService.ts
import ApiService from './api';
import { Todo, ApiResponse } from '@/types';

class TodoService extends ApiService {
  private readonly todoBaseUrl: string;

  constructor() {
    super();
    this.todoBaseUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v2';
  }

  private async makeAuthenticatedRequest<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    try {
      // Get the JWT token from localStorage (stored by authService)
      const token = localStorage.getItem('accessToken');

      const headers = {
        'Content-Type': 'application/json',
        ...(token && { 'Authorization': `Bearer ${token}` }),
        ...options.headers,
      };

      const response = await fetch(`${this.todoBaseUrl}${endpoint}`, {
        ...options,
        headers,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        return {
          success: false,
          error: {
            message: errorData.detail || `HTTP error! status: ${response.status}`,
            code: 'API_ERROR'
          }
        };
      }

      // Handle responses with no body (like 204 No Content)
      if (response.status === 204) {
        return {
          success: true,
          data: undefined as T // Return undefined for 204 responses
        };
      }

      const data = await response.json();
      return {
        success: true,
        data: data
      };
    } catch (error) {
      return {
        success: false,
        error: {
          message: error instanceof Error ? error.message : 'Network error occurred',
          code: 'NETWORK_ERROR'
        }
      };
    }
  }

  async getTodos(userId: string, filters?: { completed?: boolean; priority?: 'low' | 'medium' | 'high' }): Promise<ApiResponse<Todo[]>> {
    let endpoint = `/users/${userId}/tasks`;

    // Add query parameters for filtering if needed
    const queryParams = new URLSearchParams();
    if (filters?.completed !== undefined) {
      queryParams.append('completed', String(filters.completed));
    }

    if (queryParams.toString()) {
      endpoint += `?${queryParams.toString()}`;
    }

    return this.makeAuthenticatedRequest<Todo[]>(endpoint, {
      method: 'GET',
    });
  }

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

    const todoData = {
      title: title.trim(),
      description: description || '',
      completed: false,
      priority,
      due_date: dueDate ? dueDate.toISOString() : null,
    };

    return this.makeAuthenticatedRequest<Todo>(`/users/${userId}/tasks`, {
      method: 'POST',
      body: JSON.stringify(todoData),
    });
  }

  async updateTodo(todoId: string, updates: Partial<Todo>): Promise<ApiResponse<Todo>> {
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

    // Find user ID from auth context (assuming we have access to it)
    // In a real implementation, this would come from the auth context or similar
    const token = localStorage.getItem('accessToken');
    if (!token) {
      return {
        success: false,
        error: {
          message: 'Authentication required',
          code: 'AUTH_ERROR'
        }
      };
    }

    // We need to get the user ID from somewhere - for now, let's assume we can decode the JWT or have it elsewhere
    // For this implementation, we'll need to get the user ID from the auth context
    // Since this is called from the TodosPage, we'll need to pass the user ID

    // This is a limitation of the current approach - we need to refactor to pass the userId
    // For now, we'll return an error to indicate this needs to be addressed
    return {
      success: false,
      error: {
        message: 'User ID required for update operation',
        code: 'MISSING_USER_ID'
      }
    };
  }

  // Specialized update method that accepts userId
  async updateTodoWithUserId(userId: string, todoId: string, updates: Partial<Todo>): Promise<ApiResponse<Todo>> {
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

    const updateData: any = {};
    if (updates.title !== undefined) updateData.title = updates.title;
    if (updates.description !== undefined) updateData.description = updates.description;
    if (updates.completed !== undefined) updateData.completed = updates.completed;
    if (updates.priority !== undefined) updateData.priority = updates.priority;
    if (updates.dueDate !== undefined) updateData.due_date = updates.dueDate ? new Date(updates.dueDate).toISOString() : null;

    return this.makeAuthenticatedRequest<Todo>(`/users/${userId}/tasks/${todoId}`, {
      method: 'PUT',
      body: JSON.stringify(updateData),
    });
  }

  async deleteTodo(userId: string, todoId: string): Promise<ApiResponse<undefined>> {
    return this.makeAuthenticatedRequest<undefined>(`/users/${userId}/tasks/${todoId}`, {
      method: 'DELETE',
    });
  }

  async toggleTodoCompletion(userId: string, todoId: string): Promise<ApiResponse<Todo>> {
    return this.makeAuthenticatedRequest<Todo>(`/users/${userId}/tasks/${todoId}/complete`, {
      method: 'PATCH',
    });
  }
}

export default new TodoService();