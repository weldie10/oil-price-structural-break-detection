/**
 * Frontend validation utilities.
 * 
 * Provides reusable validation functions following DRY principles:
 * - Date validation
 * - Input sanitization
 * - Error message formatting
 */

/**
 * Validates a date string in YYYY-MM-DD format.
 * 
 * @param {string} dateString - Date string to validate
 * @param {string} fieldName - Name of the field for error messages
 * @returns {Object} - { isValid: boolean, error: string|null }
 */
export const validateDate = (dateString, fieldName = 'Date') => {
  if (!dateString || typeof dateString !== 'string') {
    return {
      isValid: false,
      error: `${fieldName} is required`
    };
  }

  // Check format YYYY-MM-DD
  const dateRegex = /^\d{4}-\d{2}-\d{2}$/;
  if (!dateRegex.test(dateString)) {
    return {
      isValid: false,
      error: `${fieldName} must be in YYYY-MM-DD format`
    };
  }

  // Check if date is valid
  const date = new Date(dateString);
  if (isNaN(date.getTime())) {
    return {
      isValid: false,
      error: `${fieldName} is not a valid date`
    };
  }

  return {
    isValid: true,
    error: null
  };
};

/**
 * Validates a date range ensuring startDate <= endDate.
 * 
 * @param {string} startDate - Start date string
 * @param {string} endDate - End date string
 * @returns {Object} - { isValid: boolean, error: string|null }
 */
export const validateDateRange = (startDate, endDate) => {
  if (!startDate && !endDate) {
    return { isValid: true, error: null };
  }

  if (startDate) {
    const startValidation = validateDate(startDate, 'Start date');
    if (!startValidation.isValid) {
      return startValidation;
    }
  }

  if (endDate) {
    const endValidation = validateDate(endDate, 'End date');
    if (!endValidation.isValid) {
      return endValidation;
    }
  }

  if (startDate && endDate) {
    const start = new Date(startDate);
    const end = new Date(endDate);
    
    if (start > end) {
      return {
        isValid: false,
        error: 'Start date must be less than or equal to end date'
      };
    }
  }

  return { isValid: true, error: null };
};

/**
 * Sanitizes a string input by trimming whitespace.
 * 
 * @param {string} input - Input string to sanitize
 * @returns {string} - Sanitized string
 */
export const sanitizeString = (input) => {
  if (typeof input !== 'string') {
    return '';
  }
  return input.trim();
};

/**
 * Validates that a value is in the allowed list.
 * 
 * @param {string} value - Value to validate
 * @param {Array} allowedValues - Array of allowed values
 * @param {string} fieldName - Name of the field for error messages
 * @returns {Object} - { isValid: boolean, error: string|null }
 */
export const validateEnum = (value, allowedValues, fieldName = 'Value') => {
  if (!value) {
    return { isValid: true, error: null }; // Empty is allowed (means "all")
  }

  if (!Array.isArray(allowedValues) || allowedValues.length === 0) {
    return {
      isValid: false,
      error: `No allowed values defined for ${fieldName}`
    };
  }

  if (!allowedValues.includes(value)) {
    return {
      isValid: false,
      error: `Invalid ${fieldName}. Allowed values: ${allowedValues.join(', ')}`
    };
  }

  return { isValid: true, error: null };
};
