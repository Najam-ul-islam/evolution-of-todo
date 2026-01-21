/**
 * API service for authenticated communication with the backend chat endpoint
 * Handles making authenticated requests to /api/{user_id}/chat
 */

// Define types for better type safety
interface ErrorResponse {
  error: string;
  message?: string;
  details?: any;
}

/**
 * Send a message to the backend chat endpoint with proper authentication
 * @param request The message request containing message text and optional conversation_id
 * @param userId The user ID for the API endpoint
 * @param token The authentication token
 * @returns Promise resolving to the response from the backend
 * @throws Error if the request fails
 */
export const sendAuthenticatedMessage = async (
  request: { message: string; conversation_id?: string },
  userId: string,
  token: string
): Promise<{ response: string; conversation_id: string }> => {
  try {
    // Construct the API endpoint URL
    const apiUrl = `${process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api'}/${userId}/chat`;

    // Make the authenticated API request
    const response = await fetch(apiUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({
        message: request.message,
        conversation_id: request.conversation_id,
      }),
    });

    // Handle different response statuses
    if (!response.ok) {
      const errorData = await response.json().catch(() => ({
        error: 'Unknown error',
        message: `HTTP error! Status: ${response.status}`,
      }));

      throw new Error(`API request failed: ${errorData.error || errorData.message || 'Unknown error'}`);
    }

    // Parse and return the successful response
    const data = await response.json();
    return data;

  } catch (error) {
    // Re-throw with additional context
    if (error instanceof Error) {
      throw new Error(`Failed to send authenticated message: ${error.message}`);
    } else {
      throw new Error('Failed to send authenticated message: Unknown error occurred');
    }
  }
};

/**
 * Type guard to check if a response is an error response
 * @param response The response object to check
 * @returns True if the response is an error response, false otherwise
 */
export const isErrorReponse = (response: any): response is ErrorResponse => {
  return response && typeof response === 'object' && 'error' in response;
};