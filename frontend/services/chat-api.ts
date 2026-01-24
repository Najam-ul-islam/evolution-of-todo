/**
 * API service for authenticated communication with the backend chat endpoint
 * Handles making authenticated requests to /api/{user_id}/chat
 */

// Define types for better type safety
interface ToolCallSchema {
  tool_name: string;
  tool_input: Record<string, any>;
  result?: Record<string, any>;
}

interface ChatResponse {
  response: string;
  conversation_id: number;
  tool_calls: ToolCallSchema[];
}

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
  request: { message: string; conversation_id?: string | number },
  userId: string,
  token: string
): Promise<ChatResponse> => {
  try {
    // Convert conversation_id to proper format if provided
    let processedConversationId: number | undefined = undefined;
    if (request.conversation_id !== undefined && request.conversation_id !== null) {
      if (typeof request.conversation_id === 'string') {
        // Try to parse the string as an integer
        const parsedId = parseInt(request.conversation_id, 10);
        if (isNaN(parsedId) || parsedId <= 0) {
          console.warn(`Invalid conversation ID string: "${request.conversation_id}", starting new conversation`);
          processedConversationId = undefined;
        } else {
          processedConversationId = parsedId;
        }
      } else if (typeof request.conversation_id === 'number') {
        if (request.conversation_id <= 0) {
          console.warn(`Invalid conversation ID number: ${request.conversation_id}, starting new conversation`);
          processedConversationId = undefined;
        } else {
          processedConversationId = request.conversation_id;
        }
      }
    }

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
        conversation_id: processedConversationId,
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