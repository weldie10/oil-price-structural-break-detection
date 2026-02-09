/**
 * Frontend error handling utilities.
 * 
 * Provides consistent error handling and user-friendly error messages:
 * - API error parsing
 * - Error message formatting
 * - Error logging
 */

/**
 * Extracts a user-friendly error message from an API error response.
 * 
 * @param {Error} error - Error object from API call
 * @returns {string} - User-friendly error message
 */
export const getErrorMessage = (error) => {
  if (!error) {
    return 'An unknown error occurred';
  }

  // Handle axios errors
  if (error.response) {
    const { data, status, statusText } = error.response;
    
    // Try to get error message from response data
    if (data && data.error) {
      return data.error;
    }
    
    // Fallback to status text
    if (statusText) {
      return `${statusText} (${status})`;
    }
    
    // Generic status-based messages
    switch (status) {
      case 400:
        return 'Invalid request. Please check your input and try again.';
      case 401:
        return 'Authentication required. Please log in.';
      case 403:
        return 'You do not have permission to access this resource.';
      case 404:
        return 'The requested resource was not found.';
      case 500:
        return 'Server error. Please try again later.';
      case 503:
        return 'Service temporarily unavailable. Please try again later.';
      default:
        return `Server error (${status}). Please try again.`;
    }
  }

  // Handle network errors
  if (error.request) {
    return 'Unable to connect to the server. Please check your internet connection.';
  }

  // Handle other errors
  if (error.message) {
    return error.message;
  }

  return 'An unexpected error occurred. Please try again.';
};

/**
 * Logs an error with context information.
 * 
 * @param {Error} error - Error object
 * @param {string} context - Context where error occurred
 * @param {Object} additionalInfo - Additional information to log
 */
export const logError = (error, context = 'Application', additionalInfo = {}) => {
  const errorMessage = getErrorMessage(error);
  
  console.error(`[${context}] Error:`, {
    message: errorMessage,
    originalError: error,
    ...additionalInfo,
    timestamp: new Date().toISOString()
  });
};

/**
 * Creates a standardized error object.
 * 
 * @param {string} message - Error message
 * @param {string} code - Error code
 * @param {Object} details - Additional error details
 * @returns {Object} - Standardized error object
 */
export const createError = (message, code = 'UNKNOWN_ERROR', details = {}) => {
  return {
    message,
    code,
    details,
    timestamp: new Date().toISOString()
  };
};

/**
 * Checks if an error is a validation error.
 * 
 * @param {Error} error - Error object
 * @returns {boolean} - True if validation error
 */
export const isValidationError = (error) => {
  if (error.response && error.response.data) {
    const errorType = error.response.data.error_type;
    return errorType === 'ValidationError' || error.response.status === 400;
  }
  return false;
};

/**
 * Checks if an error is a network error.
 * 
 * @param {Error} error - Error object
 * @returns {boolean} - True if network error
 */
export const isNetworkError = (error) => {
  return !error.response && error.request;
};
