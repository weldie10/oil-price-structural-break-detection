import React from 'react';
import './EventList.css';

function EventList({ events }) {
  if (!events || events.length === 0) {
    return (
      <div className="event-list-container">
        <h3>Events</h3>
        <p className="no-events">No events found for the selected filters</p>
      </div>
    );
  }

  const getEventColor = (event) => {
    if (event.severity === 'Very High') return '#e74c3c';
    if (event.severity === 'High') return '#f39c12';
    if (event.severity === 'Medium') return '#3498db';
    return '#95a5a6';
  };

  return (
    <div className="event-list-container">
      <h3>Events ({events.length})</h3>
      <div className="events-list">
        {events.map((event, index) => (
          <div
            key={index}
            className="event-item"
            style={{ borderLeftColor: getEventColor(event) }}
          >
            <div className="event-header">
              <span className="event-date">{event.event_date}</span>
              {event.severity && (
                <span
                  className="event-severity"
                  style={{ backgroundColor: getEventColor(event) }}
                >
                  {event.severity}
                </span>
              )}
            </div>
            <div className="event-type">{event.event_type || 'Unknown'}</div>
            <div className="event-description">
              {event.event_description || 'No description available'}
            </div>
            {event.impact_type && (
              <div className="event-impact">
                Impact: {event.impact_type}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}

export default EventList;
