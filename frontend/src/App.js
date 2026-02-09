import React, { useState, useEffect } from 'react';
import './App.css';
import PriceChart from './components/PriceChart';
import EventList from './components/EventList';
import StatisticsPanel from './components/StatisticsPanel';
import Filters from './components/Filters';
import { fetchPriceData, fetchEvents, fetchStatistics, fetchEventCorrelation } from './services/api';

function App() {
  const [priceData, setPriceData] = useState(null);
  const [events, setEvents] = useState([]);
  const [statistics, setStatistics] = useState(null);
  const [filters, setFilters] = useState({
    startDate: '2000-01-01',
    endDate: new Date().toISOString().split('T')[0],
    eventType: 'all',
    impactType: 'all'
  });
  const [selectedEvent, setSelectedEvent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadData();
  }, [filters]);

  const loadData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const [priceDataResult, eventsResult, statsResult] = await Promise.all([
        fetchPriceData(filters.startDate, filters.endDate),
        fetchEvents(filters.startDate, filters.endDate, filters.eventType, filters.impactType),
        fetchStatistics()
      ]);

      setPriceData(priceDataResult);
      setEvents(eventsResult);
      setStatistics(statsResult);
    } catch (err) {
      setError(err.message);
      console.error('Error loading data:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (newFilters) => {
    setFilters(prev => ({ ...prev, ...newFilters }));
  };

  const handleEventSelect = (event) => {
    setSelectedEvent(event);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Oil Price Structural Break Dashboard</h1>
        <p>Interactive analysis of Brent crude oil prices and market events</p>
      </header>

      <div className="App-container">
        <aside className="App-sidebar">
          <Filters 
            filters={filters} 
            onFilterChange={handleFilterChange}
          />
          
          <StatisticsPanel 
            statistics={statistics}
            loading={loading}
          />
        </aside>

        <main className="App-main">
          {error && (
            <div className="error-message">
              <p>Error: {error}</p>
              <button onClick={loadData}>Retry</button>
            </div>
          )}

          {loading ? (
            <div className="loading">Loading data...</div>
          ) : (
            <>
              <PriceChart 
                priceData={priceData}
                events={events}
                selectedEvent={selectedEvent}
                onEventSelect={handleEventSelect}
              />

              <EventList 
                events={events}
                selectedEvent={selectedEvent}
                onEventSelect={handleEventSelect}
              />
            </>
          )}
        </main>
      </div>
    </div>
  );
}

export default App;
