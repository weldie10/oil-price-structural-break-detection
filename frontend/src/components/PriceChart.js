import React, { useMemo } from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  ReferenceLine
} from 'recharts';
import './PriceChart.css';

const PriceChart = ({ priceData, events, selectedEvent, onEventSelect }) => {
  const chartData = useMemo(() => {
    if (!priceData || !priceData.dates || !priceData.prices) {
      return [];
    }

    return priceData.dates.map((date, index) => ({
      date: date,
      price: priceData.prices[index] || 0,
      timestamp: new Date(date).getTime()
    }));
  }, [priceData]);

  const eventMarkers = useMemo(() => {
    if (!events || !priceData) return [];

    return events.map(event => {
      const eventDate = new Date(event.event_date).getTime();
      const pricePoint = chartData.find(
        point => Math.abs(point.timestamp - eventDate) < 86400000 // Within 1 day
      );

      return {
        date: event.event_date,
        price: pricePoint ? pricePoint.price : null,
        event: event,
        severity: event.severity || 'Medium'
      };
    }).filter(marker => marker.price !== null);
  }, [events, chartData]);

  const getEventColor = (severity) => {
    switch (severity) {
      case 'Very High': return '#ff0000';
      case 'High': return '#ff8800';
      case 'Medium': return '#888888';
      default: return '#cccccc';
    }
  };


  if (!priceData || chartData.length === 0) {
    return (
      <div className="chart-container">
        <div className="chart-placeholder">
          <p>No price data available. Please ensure the backend is running and data is loaded.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="chart-container">
      <div className="chart-header">
        <h2>Brent Crude Oil Price Over Time</h2>
        <p>Click on event markers to see details</p>
      </div>
      
      <ResponsiveContainer width="100%" height={500}>
        <LineChart data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 80 }}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis 
            dataKey="date" 
            angle={-45}
            textAnchor="end"
            height={100}
            interval="preserveStartEnd"
            tickFormatter={(value) => {
              const date = new Date(value);
              return `${date.getMonth() + 1}/${date.getFullYear()}`;
            }}
          />
          <YAxis 
            label={{ value: 'Price (USD/barrel)', angle: -90, position: 'insideLeft' }}
          />
          <Tooltip 
            formatter={(value) => [`$${value.toFixed(2)}`, 'Price']}
            labelFormatter={(label) => `Date: ${label}`}
            contentStyle={{
              backgroundColor: 'rgba(255, 255, 255, 0.95)',
              border: '1px solid #ccc',
              borderRadius: '4px'
            }}
          />
          <Legend />
          <Line 
            type="monotone" 
            dataKey="price" 
            stroke="#667eea" 
            strokeWidth={2}
            dot={false}
            name="Brent Crude Price"
          />
          
          {/* Event markers as reference lines */}
          {eventMarkers.map((marker, index) => (
            <ReferenceLine
              key={index}
              x={marker.date}
              stroke={getEventColor(marker.severity)}
              strokeDasharray="3 3"
              strokeWidth={2}
              label={{
                value: marker.event.event_type || 'Event',
                position: 'top',
                fill: getEventColor(marker.severity),
                fontSize: 10
              }}
            />
          ))}
        </LineChart>
      </ResponsiveContainer>

      {selectedEvent && (
        <div className="event-details">
          <h3>Selected Event Details</h3>
          <div className="event-info">
            <p><strong>Description:</strong> {selectedEvent.event_description}</p>
            <p><strong>Date:</strong> {selectedEvent.event_date}</p>
            <p><strong>Type:</strong> {selectedEvent.event_type}</p>
            <p><strong>Impact:</strong> {selectedEvent.impact_type}</p>
            <p><strong>Severity:</strong> {selectedEvent.severity}</p>
          </div>
        </div>
      )}
    </div>
  );
};

export default PriceChart;
