/**
 * Data transformation utilities.
 * 
 * Provides reusable functions for data manipulation:
 * - Date formatting
 * - Number formatting
 * - Data structure transformations
 */

/**
 * Formats a date string for display.
 * 
 * @param {string} dateString - Date string in YYYY-MM-DD format
 * @param {Object} options - Formatting options
 * @returns {string} - Formatted date string
 */
export const formatDate = (dateString, options = {}) => {
  if (!dateString) {
    return '';
  }

  try {
    const date = new Date(dateString);
    if (isNaN(date.getTime())) {
      return dateString; // Return original if invalid
    }

    const {
      year = 'numeric',
      month = 'short',
      day = 'numeric',
      locale = 'en-US'
    } = options;

    return date.toLocaleDateString(locale, { year, month, day });
  } catch (error) {
    console.warn('Error formatting date:', error);
    return dateString;
  }
};

/**
 * Formats a number as currency.
 * 
 * @param {number} value - Number to format
 * @param {string} currency - Currency code (default: USD)
 * @param {Object} options - Formatting options
 * @returns {string} - Formatted currency string
 */
export const formatCurrency = (value, currency = 'USD', options = {}) => {
  if (value === null || value === undefined || isNaN(value)) {
    return 'N/A';
  }

  try {
    const {
      minimumFractionDigits = 2,
      maximumFractionDigits = 2,
      locale = 'en-US'
    } = options;

    return new Intl.NumberFormat(locale, {
      style: 'currency',
      currency,
      minimumFractionDigits,
      maximumFractionDigits
    }).format(value);
  } catch (error) {
    console.warn('Error formatting currency:', error);
    return `$${value.toFixed(2)}`;
  }
};

/**
 * Formats a number with specified decimal places.
 * 
 * @param {number} value - Number to format
 * @param {number} decimals - Number of decimal places
 * @returns {string} - Formatted number string
 */
export const formatNumber = (value, decimals = 2) => {
  if (value === null || value === undefined || isNaN(value)) {
    return 'N/A';
  }

  return value.toFixed(decimals);
};

/**
 * Formats a percentage value.
 * 
 * @param {number} value - Percentage value (0-100)
 * @param {number} decimals - Number of decimal places
 * @returns {string} - Formatted percentage string
 */
export const formatPercentage = (value, decimals = 2) => {
  if (value === null || value === undefined || isNaN(value)) {
    return 'N/A';
  }

  return `${value.toFixed(decimals)}%`;
};

/**
 * Safely gets a nested property from an object.
 * 
 * @param {Object} obj - Object to access
 * @param {string} path - Dot-separated path to property
 * @param {*} defaultValue - Default value if property doesn't exist
 * @returns {*} - Property value or default
 */
export const getNestedProperty = (obj, path, defaultValue = null) => {
  if (!obj || !path) {
    return defaultValue;
  }

  const keys = path.split('.');
  let value = obj;

  for (const key of keys) {
    if (value === null || value === undefined) {
      return defaultValue;
    }
    value = value[key];
  }

  return value !== undefined ? value : defaultValue;
};

/**
 * Checks if a value is empty (null, undefined, empty string, empty array).
 * 
 * @param {*} value - Value to check
 * @returns {boolean} - True if value is empty
 */
export const isEmpty = (value) => {
  if (value === null || value === undefined) {
    return true;
  }
  if (typeof value === 'string') {
    return value.trim() === '';
  }
  if (Array.isArray(value)) {
    return value.length === 0;
  }
  if (typeof value === 'object') {
    return Object.keys(value).length === 0;
  }
  return false;
};
