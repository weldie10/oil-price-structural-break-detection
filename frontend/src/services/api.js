import axios from 'axios';
import { logError } from '../utils/errorHandling';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 second timeout
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    // Log request in development
    if (process.env.NODE_ENV === 'development') {
      console.log(`[API Request] ${config.method.toUpperCase()} ${config.url}`, config.params);
    }
    return config;
  },
  (error) => {
    logError(error, 'API Request Interceptor');
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    // Log successful response in development
    if (process.env.NODE_ENV === 'development') {
      console.log(`[API Response] ${response.config.method.toUpperCase()} ${response.config.url}`, response.status);
    }
    return response;
  },
  (error) => {
    // Enhanced error logging
    logError(error, 'API Response Interceptor', {
      url: error.config?.url,
      method: error.config?.method,
      status: error.response?.status
    });
    return Promise.reject(error);
  }
);

export default {
  getPriceData: (params = {}) => {
    return api.get('/price-data', { params });
  },
  
  getEvents: (params = {}) => {
    return api.get('/events', { params });
  },
  
  getEventFilters: () => {
    return api.get('/event-filters');
  },
  
  getStatistics: (params = {}) => {
    return api.get('/statistics', { params });
  },
  
  healthCheck: () => {
    return api.get('/health');
  },
};
