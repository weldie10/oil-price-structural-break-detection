import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const fetchPriceData = async (startDate, endDate, frequency = 'D') => {
  try {
    const response = await api.get('/price-data', {
      params: { start_date: startDate, end_date: endDate, frequency }
    });
    return response.data;
  } catch (error) {
    throw new Error(`Failed to fetch price data: ${error.message}`);
  }
};

export const fetchEvents = async (startDate, endDate, eventType = 'all', impactType = 'all') => {
  try {
    const params = { start_date: startDate, end_date: endDate };
    if (eventType !== 'all') params.event_type = eventType;
    if (impactType !== 'all') params.impact_type = impactType;
    
    const response = await api.get('/events', { params });
    return response.data;
  } catch (error) {
    throw new Error(`Failed to fetch events: ${error.message}`);
  }
};

export const fetchChangePoints = async () => {
  try {
    const response = await api.get('/change-points');
    return response.data;
  } catch (error) {
    throw new Error(`Failed to fetch change points: ${error.message}`);
  }
};

export const fetchEventCorrelation = async () => {
  try {
    const response = await api.get('/event-correlation');
    return response.data;
  } catch (error) {
    throw new Error(`Failed to fetch event correlation: ${error.message}`);
  }
};

export const fetchStatistics = async () => {
  try {
    const response = await api.get('/statistics');
    return response.data;
  } catch (error) {
    throw new Error(`Failed to fetch statistics: ${error.message}`);
  }
};

export const fetchEventImpact = async (eventId, windowDays = 30) => {
  try {
    const response = await api.get(`/event-impact/${eventId}`, {
      params: { window_days: windowDays }
    });
    return response.data;
  } catch (error) {
    throw new Error(`Failed to fetch event impact: ${error.message}`);
  }
};
