import React from 'react';
import './Filters.css';

const Filters = ({ filters, onFilterChange }) => {
  const handleDateChange = (field, value) => {
    onFilterChange({ [field]: value });
  };

  const handleTypeChange = (field, value) => {
    onFilterChange({ [field]: value });
  };

  return (
    <div className="filters-container">
      <h3>Filters</h3>
      
      <div className="filter-group">
        <label htmlFor="start-date">Start Date</label>
        <input
          id="start-date"
          type="date"
          value={filters.startDate}
          onChange={(e) => handleDateChange('startDate', e.target.value)}
        />
      </div>

      <div className="filter-group">
        <label htmlFor="end-date">End Date</label>
        <input
          id="end-date"
          type="date"
          value={filters.endDate}
          onChange={(e) => handleDateChange('endDate', e.target.value)}
        />
      </div>

      <div className="filter-group">
        <label htmlFor="event-type">Event Type</label>
        <select
          id="event-type"
          value={filters.eventType}
          onChange={(e) => handleTypeChange('eventType', e.target.value)}
        >
          <option value="all">All Types</option>
          <option value="OPEC">OPEC</option>
          <option value="Geopolitical">Geopolitical</option>
          <option value="Economic">Economic</option>
          <option value="Natural Disaster">Natural Disaster</option>
          <option value="Market">Market</option>
          <option value="Pandemic">Pandemic</option>
        </select>
      </div>

      <div className="filter-group">
        <label htmlFor="impact-type">Impact Type</label>
        <select
          id="impact-type"
          value={filters.impactType}
          onChange={(e) => handleTypeChange('impactType', e.target.value)}
        >
          <option value="all">All Impacts</option>
          <option value="Supply Shock">Supply Shock</option>
          <option value="Demand Shock">Demand Shock</option>
          <option value="Market">Market</option>
          <option value="Geopolitical">Geopolitical</option>
        </select>
      </div>
    </div>
  );
};

export default Filters;
