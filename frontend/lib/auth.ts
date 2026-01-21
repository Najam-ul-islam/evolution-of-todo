/**
 * Authentication utilities for Better Auth integration
 * Provides functions to extract user context for API calls
 */

// Import not needed for this utility file
// We're providing functions that can be used with session data

/**
 * Extract user_id and jwt token from Better Auth session
 * @returns Object containing user_id and jwt_token if available, null otherwise
 */
export const getUserContext = () => {
  // This is a utility function that can be called to get the current user context
  // For server-side usage, we'd need to use getServerSession

  // For client-side usage, the session would be accessed via the useStore hook
  // This function is exported for use in API service layers
  return {
    getUserId: (sessionData: any): string | null => {
      // Extract user ID from the session object
      const session = sessionData?.data || sessionData;
      return session?.user?.id || null;
    },
    getJwtToken: (sessionData: any): string | null => {
      // Extract JWT token from the session object
      // Better Auth typically provides a token property
      const session = sessionData?.data || sessionData;
      return session?.token || session?.accessToken || null;
    }
  };
};

/**
 * For server-side usage (in API routes or server components)
 * This would be used to get session server-side
 */
export const getServerUserContext = async () => {
  // Placeholder for server-side session retrieval
  // Actual implementation would use Better Auth server-side methods
  try {
    // const session = await getServerSession(); // This would use Better Auth's server-side session
    // return {
    //   userId: session?.user?.id || null,
    //   jwtToken: session?.accessToken || null
    // };

    // For now returning a placeholder structure
    return {
      userId: null,
      jwtToken: null
    };
  } catch (error) {
    console.error('Error getting server user context:', error);
    return {
      userId: null,
      jwtToken: null
    };
  }
};