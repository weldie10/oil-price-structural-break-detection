# Oil Price Dashboard - Frontend

React-based dashboard for visualizing oil price data, events, and structural breaks.

## Features

- **Interactive Price Chart**: Plotly-based visualization with event highlighting
- **Date Range Filters**: Filter price data by start and end dates
- **Event Filters**: Filter events by type, impact type, and severity
- **Event Highlighting**: Visual markers on the chart showing event locations
- **Statistics Panel**: Real-time price statistics for the selected date range
- **Event List**: Scrollable list of events with details
- **Responsive Design**: Works on desktop, tablet, and mobile devices

## Setup

### Prerequisites

- Node.js 16+ and npm
- Backend API running on port 5000 (see backend/README.md)

### Installation

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The app will open at `http://localhost:3000`

### Building for Production

```bash
npm run build
```

This creates an optimized production build in the `build/` directory.

## Project Structure

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── components/
│   │   ├── Filters.js          # Date range and event filters
│   │   ├── PriceChart.js       # Interactive price chart with events
│   │   ├── Statistics.js       # Price statistics panel
│   │   └── EventList.js        # Event list component
│   ├── services/
│   │   └── api.js              # API service layer
│   ├── App.js                  # Main app component
│   ├── App.css                 # Main app styles
│   ├── index.js                # Entry point
│   └── index.css               # Global styles
├── package.json
└── README.md
```

## Usage

1. **Date Range Filtering**: Use the start date and end date inputs to filter price data
2. **Event Filtering**: Use the dropdown menus to filter events by:
   - Event Type (OPEC, Geopolitical, Economic, etc.)
   - Impact Type (Supply Shock, Demand Shock, etc.)
   - Severity (Very High, High, Medium)
3. **View Events on Chart**: Events are automatically highlighted on the price chart with:
   - Vertical dashed lines indicating event dates
   - Diamond markers at the event price point
   - Color coding based on severity or event type
4. **View Statistics**: Price statistics update automatically based on the selected date range
5. **View Event Details**: Scroll through the event list to see detailed information

## Responsive Design

The dashboard is fully responsive with breakpoints at:
- **Desktop**: > 1024px - Side-by-side layout
- **Tablet**: 768px - 1024px - Stacked layout
- **Mobile**: < 768px - Single column, optimized for touch

## API Integration

The frontend communicates with the Flask backend API. Ensure the backend is running before starting the frontend.

API endpoints used:
- `GET /api/price-data` - Get price data with date filtering
- `GET /api/events` - Get events with filtering
- `GET /api/event-filters` - Get available filter options
- `GET /api/statistics` - Get price statistics

## Technologies

- **React 18**: UI framework
- **React Plotly.js**: Interactive charts
- **Axios**: HTTP client
- **CSS Grid/Flexbox**: Responsive layout
- **CSS Media Queries**: Mobile responsiveness
