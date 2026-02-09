import React, { useMemo } from 'react';
import Plot from 'react-plotly.js';
import './PriceChart.css';

function PriceChart({ priceData, events }) {
  const getEventColor = (event) => {
    // Color coding based on event type or severity
    if (event.severity === 'Very High') return '#e74c3c';
    if (event.severity === 'High') return '#f39c12';
    if (event.severity === 'Medium') return '#3498db';
    
    if (event.event_type === 'OPEC') return '#9b59b6';
    if (event.event_type === 'Geopolitical') return '#e74c3c';
    if (event.event_type === 'Economic') return '#f39c12';
    if (event.event_type === 'Natural Disaster') return '#16a085';
    
    return '#95a5a6';
  };

  const { data, layout } = useMemo(() => {
    if (!priceData || !priceData.dates || !priceData.prices) {
      return { data: [], layout: {} };
    }

    // Prepare data for Plotly
    const trace = {
      x: priceData.dates,
      y: priceData.prices,
      type: 'scatter',
      mode: 'lines',
      name: 'Brent Crude Price',
      line: {
        color: '#3498db',
        width: 2
      },
      hovertemplate: '<b>Date:</b> %{x}<br><b>Price:</b> $%{y:.2f}<extra></extra>'
    };

    // Add event markers
    const eventTraces = [];
    if (events && events.length > 0) {
      const minPrice = Math.min(...priceData.prices);
      const maxPrice = Math.max(...priceData.prices);
      
      events.forEach((event) => {
        const eventDate = event.event_date;
        const priceIndex = priceData.dates.findIndex(d => d === eventDate);
        
        if (priceIndex !== -1) {
          const eventPrice = priceData.prices[priceIndex];
          const eventColor = getEventColor(event);
          
          // Create vertical line for event
          eventTraces.push({
            x: [eventDate, eventDate],
            y: [minPrice, maxPrice],
            type: 'scatter',
            mode: 'lines',
            name: event.event_description || event.event_type || 'Event',
            line: {
              color: eventColor,
              width: 2,
              dash: 'dash'
            },
            showlegend: false,
            hoverinfo: 'skip'
          });
          
          // Create marker for event
          eventTraces.push({
            x: [eventDate],
            y: [eventPrice],
            type: 'scatter',
            mode: 'markers+text',
            name: event.event_description || event.event_type || 'Event',
            marker: {
              color: eventColor,
              size: 12,
              symbol: 'diamond',
              line: {
                color: 'white',
                width: 2
              }
            },
            text: [event.event_type || 'Event'],
            textposition: 'top center',
            textfont: {
              size: 10,
              color: eventColor
            },
            hovertemplate: 
              `<b>Event:</b> ${event.event_description || event.event_type || 'Event'}<br>` +
              `<b>Date:</b> ${eventDate}<br>` +
              `<b>Type:</b> ${event.event_type || 'N/A'}<br>` +
              `<b>Impact:</b> ${event.impact_type || 'N/A'}<br>` +
              `<b>Severity:</b> ${event.severity || 'N/A'}<br>` +
              `<b>Price:</b> $${eventPrice?.toFixed(2) || 'N/A'}<extra></extra>`,
            showlegend: true
          });
        }
      });
    }

    const chartData = [trace, ...eventTraces];

    const chartLayout = {
      title: {
        text: 'Brent Crude Oil Price with Events',
        font: { size: 18, color: '#2c3e50' }
      },
      xaxis: {
        title: 'Date',
        showgrid: true,
        gridcolor: '#e0e0e0'
      },
      yaxis: {
        title: 'Price (USD)',
        showgrid: true,
        gridcolor: '#e0e0e0'
      },
      hovermode: 'closest',
      plot_bgcolor: 'white',
      paper_bgcolor: 'white',
      margin: { l: 60, r: 30, t: 60, b: 60 },
      legend: {
        orientation: 'h',
        y: -0.2,
        x: 0.5,
        xanchor: 'center'
      }
    };

    return { data: chartData, layout: chartLayout };
  }, [priceData, events]);

  const config = {
    responsive: true,
    displayModeBar: true,
    modeBarButtonsToRemove: ['pan2d', 'lasso2d'],
    displaylogo: false
  };

  if (!priceData || !priceData.dates || !priceData.prices) {
    return (
      <div className="chart-placeholder">
        <p>No price data available</p>
      </div>
    );
  }

  return (
    <div className="price-chart-container">
      <Plot
        data={data}
        layout={layout}
        config={config}
        style={{ width: '100%', height: '100%' }}
      />
    </div>
  );
}

export default PriceChart;
