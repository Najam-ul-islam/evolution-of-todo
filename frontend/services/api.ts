// services/api.ts
import { ApiResponse } from '@/types';

// Helper to simulate network delay
export const delay = (min: number, max: number): Promise<void> => {
  const delayMs = Math.floor(Math.random() * (max - min + 1)) + min;
  return new Promise(resolve => setTimeout(resolve, delayMs));
};

// Base API service class
class ApiService {
  private baseUrl: string;
  protected mockDelayMin: number;
  protected mockDelayMax: number;

  constructor() {
    this.baseUrl = process.env.NEXT_PUBLIC_BASE_URL || 'http://localhost:3000';
    this.mockDelayMin = parseInt(process.env.NEXT_PUBLIC_API_MOCK_DELAY_MIN || '500', 10);
    this.mockDelayMax = parseInt(process.env.NEXT_PUBLIC_API_MOCK_DELAY_MAX || '1500', 10);
  }

  // TODO: Replace with real HTTP request implementation when connecting to backend
  // Example: Use fetch or axios to make actual API calls with proper error handling
  // Include JWT token in Authorization header when available
  // SECURITY TODO: Add proper request validation and sanitization
  protected async mockApiCall<T>(response: T, success: boolean = true): Promise<ApiResponse<T>> {
    await delay(this.mockDelayMin, this.mockDelayMax);

    if (success) {
      return {
        success: true,
        data: response
      };
    } else {
      return {
        success: false,
        error: {
          message: 'Mock error occurred',
          code: 'MOCK_ERROR'
        }
      };
    }
  }

  // TODO: Replace with real HTTP request implementation when connecting to backend
  // Example: Use fetch or axios to make actual API calls with proper error handling
  protected async mockApiCallWithPossibleFailure<T>(
    response: T,
    failureRate: number = 0.1 // 10% failure rate by default
  ): Promise<ApiResponse<T>> {
    await delay(this.mockDelayMin, this.mockDelayMax);

    const shouldFail = Math.random() < failureRate;

    if (!shouldFail) {
      return {
        success: true,
        data: response
      };
    } else {
      return {
        success: false,
        error: {
          message: 'Simulated API error',
          code: 'SIMULATED_ERROR'
        }
      };
    }
  }
}

export default ApiService;