import React, { useState, useEffect } from 'react';
import './App.css';
import PriceChart from './components/PriceChart';
import Filters from './components/Filters';
import Statistics from './components/Statistics';
import EventList from './components/EventList';
import api from './services/api';
import { getErrorMessage, logError, isValidationError, isNetworkError } from './utils/errorHandling';
import { validateDateRange } from './utils/validation';

function App() {
  const [priceData, setPriceData] = useState(null);
  const [events, setEvents] = useState([]);
  const [statistics, setStatistics] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  // Filter states
  const [dateRange, setDateRange] = useState({
    startDate: '',
    endDate: ''
  });
  const [eventFilters, setEventFilters] = useState({
    eventType: '',
    impactType: '',
    severity: ''
  });
  const [availableFilters, setAvailableFilters] = useState({
    event_types: [],
    impact_types: [],
    severities: []
  });

  // Load initial data
  useEffect(() => {
    loadData();
    loadEventFilters();
  }, []);

  // Reload data when filters change
  useEffect(() => {
    loadData();
  }, [dateRange, eventFilters]);

  const loadData = async () => {
    setLoading(true);
    setError(null);
    
    // Validate date range before making API calls
    const dateValidation = validateDateRange(dateRange.startDate, dateRange.endDate);
    if (!dateValidation.isValid) {
      setError(dateValidation.error);
      setLoading(false);
      return;
    }
    
    try {
      // Build query parameters with validation
      const priceParams = {};
      if (dateRange.startDate) {
        priceParams.start_date = dateRange.startDate;
      }
      if (dateRange.endDate) {
        priceParams.end_date = dateRange.endDate;
      }
      
      // Load price data with error handling
      let priceResponse;
      try {
        priceResponse = await api.getPriceData(priceParams);
        // Handle success response structure
        const priceData = priceResponse.data?.data || priceResponse.data;
        if (!priceData || !priceData.dates || !priceData.prices) {
          throw new Error('Invalid price data format received from server');
        }
        setPriceData(priceData);
      } catch (err) {
        logError(err, 'loadData - Price Data', { params: priceParams });
        if (isNetworkError(err)) {
          setError('Unable to connect to the server. Please check your connection.');
          setLoading(false);
          return;
        }
        throw err; // Re-throw to be caught by outer catch
      }
      
      // Load events with error handling
      const eventParams = { ...priceParams };
      if (eventFilters.eventType) eventParams.event_type = eventFilters.eventType;
      if (eventFilters.impactType) eventParams.impact_type = eventFilters.impactType;
      if (eventFilters.severity) eventParams.severity = eventFilters.severity;
      
      try {
        const eventResponse = await api.getEvents(eventParams);
        const eventData = eventResponse.data?.data || eventResponse.data;
        setEvents(eventData?.events || []);
      } catch (err) {
        logError(err, 'loadData - Events', { params: eventParams });
        // Don't fail completely if events fail, just log and continue
        setEvents([]);
      }
      
      // Load statistics with error handling
      try {
        const statsResponse = await api.getStatistics(priceParams);
        const statsData = statsResponse.data?.data || statsResponse.data;
        setStatistics(statsData);
      } catch (err) {
        logError(err, 'loadData - Statistics', { params: priceParams });
        // Don't fail completely if statistics fail, just log and continue
        setStatistics(null);
      }
      
    } catch (err) {
      const errorMessage = getErrorMessage(err);
      setError(errorMessage);
      logError(err, 'loadData', { dateRange, eventFilters });
    } finally {
      setLoading(false);
    }
  };

  const loadEventFilters = async () => {
    try {
      const response = await api.getEventFilters();
      const filterData = response.data?.data || response.data;
      setAvailableFilters(filterData || {
        event_types: [],
        impact_types: [],
        severities: []
      });
    } catch (err) {
      logError(err, 'loadEventFilters');
      // Set empty filters on error to prevent UI issues
      setAvailableFilters({
        event_types: [],
        impact_types: [],
        severities: []
      });
    }
  };

  const handleDateRangeChange = (newDateRange) => {
    setDateRange(newDateRange);
  };

  const handleEventFilterChange = (newFilters) => {
    setEventFilters(newFilters);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Oil Price Structural Break Detection Dashboard</h1>
      </header>
      
      <main className="App-main">
        {error && (
          <div className="error-message">
            Error: {error}
          </div>
        )}
        
        <Filters
          dateRange={dateRange}
          eventFilters={eventFilters}
          availableFilters={availableFilters}
          onDateRangeChange={handleDateRangeChange}
          onEventFilterChange={handleEventFilterChange}
        />
        
        {loading ? (
          <div className="loading">Loading data...</div>
        ) : (
          <>
            <div className="dashboard-grid">
              <div className="chart-container">
                <PriceChart
                  priceData={priceData}
                  events={events}
                />
              </div>
              
              <div className="sidebar">
                <Statistics statistics={statistics} />
                <EventList events={events} />
              </div>
            </div>
          </>
        )}
      </main>
    </div>
  );
}

export default App;
