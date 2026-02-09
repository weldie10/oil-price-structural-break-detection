import React from 'react';
import './Statistics.css';

function Statistics({ statistics }) {
  if (!statistics) {
    return (
      <div className="statistics-container">
        <h3>Statistics</h3>
        <p className="no-data">No statistics available</p>
      </div>
    );
  }

  return (
    <div className="statistics-container">
      <h3>Price Statistics</h3>
      <div className="stats-grid">
        <div className="stat-item">
          <div className="stat-label">Mean</div>
          <div className="stat-value">${statistics.mean?.toFixed(2) || 'N/A'}</div>
        </div>
        <div className="stat-item">
          <div className="stat-label">Median</div>
          <div className="stat-value">${statistics.median?.toFixed(2) || 'N/A'}</div>
        </div>
        <div className="stat-item">
          <div className="stat-label">Min</div>
          <div className="stat-value">${statistics.min?.toFixed(2) || 'N/A'}</div>
        </div>
        <div className="stat-item">
          <div className="stat-label">Max</div>
          <div className="stat-value">${statistics.max?.toFixed(2) || 'N/A'}</div>
        </div>
        <div className="stat-item">
          <div className="stat-label">Std Dev</div>
          <div className="stat-value">${statistics.std?.toFixed(2) || 'N/A'}</div>
        </div>
        <div className="stat-item">
          <div className="stat-label">Count</div>
          <div className="stat-value">{statistics.count || 'N/A'}</div>
        </div>
      </div>
    </div>
  );
}

export default Statistics;
