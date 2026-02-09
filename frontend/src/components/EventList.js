import React from 'react';
import './EventList.css';

const EventList = ({ events, selectedEvent, onEventSelect }) => {
  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'Very High': return '#ff0000';
      case 'High': return '#ff8800';
      case 'Medium': return '#888888';
      default: return '#cccccc';
    }
  };

  if (!events || events.length === 0) {
    return (
      <div className="event-list-container">
        <div className="event-list-placeholder">
          <p>No events found for the selected filters.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="event-list-container">
      <div className="event-list-header">
        <h2>Historical Events ({events.length})</h2>
      </div>
      
      <div className="event-list">
        {events.map((event, index) => (
          <div
            key={index}
            className={`event-item ${selectedEvent && selectedEvent.event_date === event.event_date ? 'selected' : ''}`}
            onClick={() => onEventSelect(event)}
            style={{
              borderLeftColor: getSeverityColor(event.severity)
            }}
          >
            <div className="event-date">
              {new Date(event.event_date).toLocaleDateString('en-US', {
                year: 'numeric',
                month: 'short',
                day: 'numeric'
              })}
            </div>
            <div className="event-description">
              {event.event_description}
            </div>
            <div className="event-meta">
              <span className="event-type">{event.event_type}</span>
              <span className="event-impact">{event.impact_type}</span>
              <span 
                className="event-severity"
                style={{ color: getSeverityColor(event.severity) }}
              >
                {event.severity}
              </span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default EventList;
