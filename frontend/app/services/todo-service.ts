'use client';

// Mock API service for todo operations
// In a real implementation, this would call actual API endpoints

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

// Define types
export interface Task {
  id: number;
  title: string;
  description?: string;
  completed: boolean;
  createdAt?: string;
  updatedAt?: string;
}

// Mock data store (in real app, this would be API calls)
let mockTasks: Task[] = [
  { id: 1, title: 'Sample Task', description: 'This is a sample task', completed: false },
  { id: 2, title: 'Another Task', description: 'This is another sample task', completed: true },
];

let nextId = 3;

// Mock API functions
export const todoService = {
  // Get all tasks
  getTasks: async (): Promise<Task[]> => {
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 300));
    return [...mockTasks]; // Return a copy to prevent direct mutation
  },

  // Get a single task by ID
  getTaskById: async (id: number): Promise<Task> => {
    await new Promise(resolve => setTimeout(resolve, 300));
    const task = mockTasks.find(t => t.id === id);
    if (!task) {
      throw new Error(`Task with id ${id} not found`);
    }
    return task;
  },

  // Create a new task
  createTask: async (title: string, description?: string): Promise<Task> => {
    await new Promise(resolve => setTimeout(resolve, 300));

    const newTask: Task = {
      id: nextId++,
      title,
      description,
      completed: false,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };

    mockTasks.push(newTask);
    return newTask;
  },

  // Update a task
  updateTask: async (id: number, title?: string, description?: string): Promise<Task> => {
    await new Promise(resolve => setTimeout(resolve, 300));

    const taskIndex = mockTasks.findIndex(t => t.id === id);
    if (taskIndex === -1) {
      throw new Error(`Task with id ${id} not found`);
    }

    const updatedTask = {
      ...mockTasks[taskIndex],
      ...(title !== undefined && { title }),
      ...(description !== undefined && { description }),
      updatedAt: new Date().toISOString(),
    };

    mockTasks[taskIndex] = updatedTask;
    return updatedTask;
  },

  // Delete a task
  deleteTask: async (id: number): Promise<boolean> => {
    await new Promise(resolve => setTimeout(resolve, 300));

    const initialLength = mockTasks.length;
    mockTasks = mockTasks.filter(t => t.id !== id);

    return mockTasks.length < initialLength;
  },

  // Toggle task completion status
  toggleTaskCompletion: async (id: number): Promise<Task> => {
    await new Promise(resolve => setTimeout(resolve, 300));

    const taskIndex = mockTasks.findIndex(t => t.id === id);
    if (taskIndex === -1) {
      throw new Error(`Task with id ${id} not found`);
    }

    const updatedTask = {
      ...mockTasks[taskIndex],
      completed: !mockTasks[taskIndex].completed,
      updatedAt: new Date().toISOString(),
    };

    mockTasks[taskIndex] = updatedTask;
    return updatedTask;
  },
};