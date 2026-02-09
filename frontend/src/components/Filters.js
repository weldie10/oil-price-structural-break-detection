import React, { useState } from 'react';
import './Filters.css';
import { validateDate, validateDateRange, sanitizeString } from '../utils/validation';

function Filters({ dateRange, eventFilters, availableFilters, onDateRangeChange, onEventFilterChange }) {
  const [dateErrors, setDateErrors] = useState({ startDate: null, endDate: null, range: null });

  const handleStartDateChange = (e) => {
    const newStartDate = sanitizeString(e.target.value);
    
    // Validate individual date
    const validation = validateDate(newStartDate, 'Start date');
    if (!validation.isValid) {
      setDateErrors(prev => ({ ...prev, startDate: validation.error, range: null }));
      return;
    }
    
    // Validate date range
    const rangeValidation = validateDateRange(newStartDate, dateRange.endDate);
    if (!rangeValidation.isValid) {
      setDateErrors(prev => ({ ...prev, startDate: null, range: rangeValidation.error }));
      return;
    }
    
    // Clear errors and update
    setDateErrors({ startDate: null, endDate: null, range: null });
    onDateRangeChange({
      ...dateRange,
      startDate: newStartDate
    });
  };

  const handleEndDateChange = (e) => {
    const newEndDate = sanitizeString(e.target.value);
    
    // Validate individual date
    const validation = validateDate(newEndDate, 'End date');
    if (!validation.isValid) {
      setDateErrors(prev => ({ ...prev, endDate: validation.error, range: null }));
      return;
    }
    
    // Validate date range
    const rangeValidation = validateDateRange(dateRange.startDate, newEndDate);
    if (!rangeValidation.isValid) {
      setDateErrors(prev => ({ ...prev, endDate: null, range: rangeValidation.error }));
      return;
    }
    
    // Clear errors and update
    setDateErrors({ startDate: null, endDate: null, range: null });
    onDateRangeChange({
      ...dateRange,
      endDate: newEndDate
    });
  };

  const handleEventTypeChange = (e) => {
    onEventFilterChange({
      ...eventFilters,
      eventType: e.target.value
    });
  };

  const handleImpactTypeChange = (e) => {
    onEventFilterChange({
      ...eventFilters,
      impactType: e.target.value
    });
  };

  const handleSeverityChange = (e) => {
    onEventFilterChange({
      ...eventFilters,
      severity: e.target.value
    });
  };

  const clearFilters = () => {
    onDateRangeChange({ startDate: '', endDate: '' });
    onEventFilterChange({ eventType: '', impactType: '', severity: '' });
  };

  return (
    <div className="filters-container">
      <div className="filters-header">
        <h2>Filters</h2>
        <button onClick={clearFilters} className="clear-button">
          Clear All
        </button>
      </div>
      
      <div className="filters-grid">
        <div className="filter-group">
          <label htmlFor="start-date">Start Date</label>
          <input
            type="date"
            id="start-date"
            value={dateRange.startDate}
            onChange={handleStartDateChange}
            className={`date-input ${dateErrors.startDate || dateErrors.range ? 'error' : ''}`}
            aria-invalid={!!(dateErrors.startDate || dateErrors.range)}
            aria-describedby={dateErrors.startDate || dateErrors.range ? 'start-date-error' : undefined}
          />
          {(dateErrors.startDate || dateErrors.range) && (
            <span id="start-date-error" className="error-message" role="alert">
              {dateErrors.startDate || dateErrors.range}
            </span>
          )}
        </div>
        
        <div className="filter-group">
          <label htmlFor="end-date">End Date</label>
          <input
            type="date"
            id="end-date"
            value={dateRange.endDate}
            onChange={handleEndDateChange}
            className={`date-input ${dateErrors.endDate || dateErrors.range ? 'error' : ''}`}
            aria-invalid={!!(dateErrors.endDate || dateErrors.range)}
            aria-describedby={dateErrors.endDate || dateErrors.range ? 'end-date-error' : undefined}
          />
          {(dateErrors.endDate || dateErrors.range) && (
            <span id="end-date-error" className="error-message" role="alert">
              {dateErrors.endDate || dateErrors.range}
            </span>
          )}
        </div>
        
        <div className="filter-group">
          <label htmlFor="event-type">Event Type</label>
          <select
            id="event-type"
            value={eventFilters.eventType}
            onChange={handleEventTypeChange}
            className="select-input"
          >
            <option value="">All Types</option>
            {availableFilters.event_types?.map(type => (
              <option key={type} value={type}>{type}</option>
            ))}
          </select>
        </div>
        
        <div className="filter-group">
          <label htmlFor="impact-type">Impact Type</label>
          <select
            id="impact-type"
            value={eventFilters.impactType}
            onChange={handleImpactTypeChange}
            className="select-input"
          >
            <option value="">All Impact Types</option>
            {availableFilters.impact_types?.map(type => (
              <option key={type} value={type}>{type}</option>
            ))}
          </select>
        </div>
        
        <div className="filter-group">
          <label htmlFor="severity">Severity</label>
          <select
            id="severity"
            value={eventFilters.severity}
            onChange={handleSeverityChange}
            className="select-input"
          >
            <option value="">All Severities</option>
            {availableFilters.severities?.map(severity => (
              <option key={severity} value={severity}>{severity}</option>
            ))}
          </select>
        </div>
      </div>
    </div>
  );
}

export default Filters;
