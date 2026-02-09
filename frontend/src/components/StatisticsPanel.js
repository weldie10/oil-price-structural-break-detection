import React from 'react';
import './StatisticsPanel.css';

const StatisticsPanel = ({ statistics, loading }) => {
  if (loading) {
    return (
      <div className="statistics-container">
        <div className="loading">Loading statistics...</div>
      </div>
    );
  }

  if (!statistics) {
    return (
      <div className="statistics-container">
        <div className="no-data">No statistics available</div>
      </div>
    );
  }

  return (
    <div className="statistics-container">
      <h3>Key Indicators</h3>
      
      {statistics.price && (
        <div className="stat-section">
          <h4>Price Statistics</h4>
          <div className="stat-item">
            <span className="stat-label">Mean Price:</span>
            <span className="stat-value">${statistics.price.mean?.toFixed(2) || 'N/A'}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Min Price:</span>
            <span className="stat-value">${statistics.price.min?.toFixed(2) || 'N/A'}</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Max Price:</span>
            <span className="stat-value">${statistics.price.max?.toFixed(2) || 'N/A'}</span>
          </div>
          {statistics.price.date_range && (
            <div className="stat-item">
              <span className="stat-label">Date Range:</span>
              <span className="stat-value">
                {statistics.price.date_range.start} to {statistics.price.date_range.end}
              </span>
            </div>
          )}
        </div>
      )}

      {statistics.volatility && (
        <div className="stat-section">
          <h4>Volatility</h4>
          <div className="stat-item">
            <span className="stat-label">Daily:</span>
            <span className="stat-value">{(statistics.volatility.daily * 100).toFixed(2)}%</span>
          </div>
          <div className="stat-item">
            <span className="stat-label">Annualized:</span>
            <span className="stat-value">{(statistics.volatility.annualized * 100).toFixed(2)}%</span>
          </div>
        </div>
      )}

      {statistics.events && (
        <div className="stat-section">
          <h4>Events</h4>
          <div className="stat-item">
            <span className="stat-label">Total Events:</span>
            <span className="stat-value">{statistics.events.total || 0}</span>
          </div>
          {statistics.events.by_severity && (
            <div className="stat-subsection">
              <strong>By Severity:</strong>
              {Object.entries(statistics.events.by_severity).map(([severity, count]) => (
                <div key={severity} className="stat-item-small">
                  {severity}: {count}
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default StatisticsPanel;
