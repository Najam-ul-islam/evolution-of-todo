// services/authService.ts
import ApiService from './api';
import { User, Session, ApiResponse } from '@/types';

interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

class AuthService extends ApiService {
  async signUp(email: string, password: string): Promise<ApiResponse<{ user: User; session: Session }>> {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api'}/auth/register`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      let responseData;
      // Check if the response is JSON before parsing
      if (response.headers.get('content-type')?.includes('application/json')) {
        responseData = await response.json();
      } else {
        // If response is not JSON, get text response
        const responseText = await response.text();
        console.warn('Response is not JSON, got:', responseText);
        // Create a generic error response
        responseData = {
          detail: responseText || 'Response is not in JSON format',
          message: responseText || 'Invalid response format'
        };
      }

      if (!response.ok) {
        // Handle different error response formats
        const errorMessage = typeof responseData === 'object' && responseData.detail
          ? responseData.detail
          : (typeof responseData === 'string' ? responseData : 'Registration failed');

        return {
          success: false,
          error: {
            message: errorMessage,
            code: 'REGISTRATION_ERROR'
          }
        };
      }

      // Type-check that responseData is the expected response format
      const data = responseData;

      // Create user object from response
      const user: User = {
        id: data.id,
        email: data.email,
        name: data.email.split('@')[0], // Use email prefix as name
        createdAt: new Date(data.created_at),
        updatedAt: new Date(data.updated_at),
        isEmailVerified: true,
      };

      // For registration, we don't automatically log the user in
      // The user will need to log in separately
      const session: Session = {
        userId: user.id,
        token: '',
        expiresAt: new Date(Date.now() + 24 * 60 * 60 * 1000), // 24 hours
        createdAt: new Date(),
      };

      return {
        success: true,
        data: { user, session }
      };
    } catch (error: any) {
      return {
        success: false,
        error: {
          message: error.message || 'Network error during registration',
          code: 'NETWORK_ERROR'
        }
      };
    }
  }

  async signIn(email: string, password: string): Promise<ApiResponse<{ user: User; session: Session }>> {
    try {
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api'}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      let responseData;
      // Check if the response is JSON before parsing
      if (response.headers.get('content-type')?.includes('application/json')) {
        responseData = await response.json();
      } else {
        // If response is not JSON, get text response
        const responseText = await response.text();
        console.warn('Response is not JSON, got:', responseText);
        // Create a generic error response
        responseData = {
          detail: responseText || 'Response is not in JSON format',
          message: responseText || 'Invalid response format'
        };
      }

      if (!response.ok) {
        // Handle different error response formats
        const errorMessage = typeof responseData === 'object' && responseData.detail
          ? responseData.detail
          : (typeof responseData === 'string' ? responseData : 'Login failed');

        return {
          success: false,
          error: {
            message: errorMessage,
            code: 'LOGIN_ERROR'
          }
        };
      }

      // Type-check that responseData is a TokenResponse
      const data: TokenResponse = responseData;

      // Store tokens in localStorage
      localStorage.setItem('accessToken', data.access_token);
      localStorage.setItem('refreshToken', data.refresh_token);

      // Get user info using the token
      const userResponse = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api'}/auth/me`, {
        headers: {
          'Authorization': `Bearer ${data.access_token}`,
        },
      });

      if (!userResponse.ok) {
        return {
          success: false,
          error: {
            message: 'Failed to fetch user information',
            code: 'USER_FETCH_ERROR'
          }
        };
      }

      let userData;
      // Check if the response is JSON before parsing
      if (userResponse.headers.get('content-type')?.includes('application/json')) {
        userData = await userResponse.json();
      } else {
        // If response is not JSON, get text response
        const responseText = await userResponse.text();
        console.warn('Response is not JSON, got:', responseText);
        // Create a generic user data response
        userData = {
          id: '',
          email: email, // Use the email from login
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
          is_active: true
        };
      }

      // Create user object from response
      const user: User = {
        id: userData.id,
        email: userData.email,
        name: userData.email.split('@')[0], // Use email prefix as name
        createdAt: new Date(userData.created_at),
        updatedAt: new Date(userData.updated_at),
        isEmailVerified: userData.is_active,
      };

      // Create session object
      const session: Session = {
        userId: user.id,
        token: data.access_token,
        expiresAt: new Date(Date.now() + 24 * 60 * 60 * 1000), // 24 hours
        createdAt: new Date(),
      };

      return {
        success: true,
        data: { user, session }
      };
    } catch (error: any) {
      return {
        success: false,
        error: {
          message: error.message || 'Network error during login',
          code: 'NETWORK_ERROR'
        }
      };
    }
  }

  async signOut(): Promise<ApiResponse<{ message: string }>> {
    try {
      // Remove tokens from localStorage
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');

      // Optionally notify the backend (though JWT is stateless)
      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api'}/auth/logout`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('accessToken')}`,
        },
      });

      // Even if the server request fails, we still clear local storage
      return {
        success: true,
        data: { message: 'Successfully signed out' }
      };
    } catch (error: any) {
      // Still clear local storage even if server request fails
      localStorage.removeItem('accessToken');
      localStorage.removeItem('refreshToken');

      return {
        success: true,
        data: { message: 'Successfully signed out' }
      };
    }
  }

  async getCurrentUser(): Promise<ApiResponse<User>> {
    try {
      const token = localStorage.getItem('accessToken');
      if (!token) {
        return {
          success: false,
          error: {
            message: 'No authentication token found',
            code: 'NO_TOKEN'
          }
        };
      }

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api'}/auth/me`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (!response.ok) {
        // If the token is invalid, remove it from storage
        if (response.status === 401) {
          localStorage.removeItem('accessToken');
          localStorage.removeItem('refreshToken');
        }

        return {
          success: false,
          error: {
            message: 'Invalid or expired token',
            code: 'TOKEN_INVALID'
          }
        };
      }

      let userData;
      // Check if the response is JSON before parsing
      if (response.headers.get('content-type')?.includes('application/json')) {
        userData = await response.json();
      } else {
        // If response is not JSON, get text response
        const responseText = await response.text();
        console.warn('Response is not JSON, got:', responseText);
        // Create a generic error response
        userData = {
          id: '',
          email: '',
          created_at: new Date().toISOString(),
          updated_at: new Date().toISOString(),
          is_active: false
        };
      }

      const user: User = {
        id: userData.id,
        email: userData.email,
        name: userData.email.split('@')[0], // Use email prefix as name
        createdAt: new Date(userData.created_at),
        updatedAt: new Date(userData.updated_at),
        isEmailVerified: userData.is_active,
      };

      return {
        success: true,
        data: user
      };
    } catch (error: any) {
      return {
        success: false,
        error: {
          message: error.message || 'Network error during user fetch',
          code: 'NETWORK_ERROR'
        }
      };
    }
  }
}

export default new AuthService();