# Interactive Dashboard - Setup Instructions

This document provides setup instructions for the Oil Price Structural Break Detection Dashboard.

## Architecture

The dashboard consists of two main components:
- **Backend**: Flask REST API (Python)
- **Frontend**: React application with Recharts visualizations

## Prerequisites

- Python 3.8+
- Node.js 16+ and npm
- Git

## Backend Setup

### 1. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

Or install globally:
```bash
pip install flask flask-cors pandas numpy
```

### 2. Run the Flask Server

```bash
cd backend
python app.py
```

The API will be available at `http://localhost:5000`

### 3. API Endpoints

The backend provides the following endpoints:

- `GET /api/health` - Health check
- `GET /api/price-data` - Get historical price data
  - Query params: `start_date`, `end_date`, `frequency`
- `GET /api/events` - Get event data
  - Query params: `start_date`, `end_date`, `event_type`, `impact_type`
- `GET /api/change-points` - Get change point results
- `GET /api/event-correlation` - Get event correlation data
- `GET /api/statistics` - Get summary statistics
- `GET /api/event-impact/<event_id>` - Get detailed impact for specific event

## Frontend Setup

### 1. Install Node Dependencies

```bash
cd frontend
npm install
```

### 2. Configure API URL (Optional)

Create a `.env` file in the `frontend` directory:

```env
REACT_APP_API_URL=http://localhost:5000/api
```

If not set, it defaults to `http://localhost:5000/api`

### 3. Run the React Development Server

```bash
cd frontend
npm start
```

The dashboard will open at `http://localhost:3000`

### 4. Build for Production

```bash
cd frontend
npm run build
```

The production build will be in the `build` directory.

## Data Requirements

### Price Data

Place your Brent crude oil price data in:
```
data/raw/brent_prices.csv
```

The CSV should have:
- Date column as index (or first column)
- Price column with numeric values

Example format:
```csv
Date,Price
2000-01-01,25.50
2000-01-02,25.75
...
```

### Event Data

Event data is already available at:
```
data/raw/oil_market_events.csv
```

## Dashboard Features

### 1. Interactive Price Chart
- Time series visualization of Brent crude oil prices
- Event markers with color coding by severity
- Click on events to see details
- Zoom and pan capabilities

### 2. Filters
- Date range selector (start and end dates)
- Event type filter (OPEC, Geopolitical, Economic, etc.)
- Impact type filter (Supply Shock, Demand Shock, etc.)

### 3. Event List
- Scrollable list of all events
- Color-coded by severity
- Click to highlight on chart
- Shows event type, impact, and severity

### 4. Statistics Panel
- Key price indicators (mean, min, max)
- Volatility metrics (daily and annualized)
- Event counts by severity
- Date range information

### 5. Event Highlight Functionality
- Click on event markers or list items
- Highlights selected event on chart
- Shows detailed event information
- Displays price impact around event date

## Responsive Design

The dashboard is responsive and works on:
- **Desktop**: Full layout with sidebar and main content
- **Tablet**: Adjusted layout with collapsible sections
- **Mobile**: Stacked layout optimized for small screens

## Troubleshooting

### Backend Issues

1. **Port already in use**: Change port in `backend/app.py`:
   ```python
   app.run(debug=True, host='0.0.0.0', port=5001)
   ```

2. **CORS errors**: Ensure `flask-cors` is installed and CORS is enabled in `app.py`

3. **Data not loading**: Check that data files exist in `data/raw/` directory

### Frontend Issues

1. **API connection errors**: 
   - Verify backend is running on port 5000
   - Check `.env` file has correct API URL
   - Check browser console for CORS errors

2. **Build errors**: 
   - Delete `node_modules` and `package-lock.json`
   - Run `npm install` again

3. **Charts not rendering**: 
   - Check browser console for errors
   - Verify Recharts is installed: `npm list recharts`

## Development

### Backend Development

The Flask app uses:
- Flask for REST API
- Flask-CORS for cross-origin requests
- Pandas for data processing
- NumPy for numerical operations

### Frontend Development

The React app uses:
- React 18 for UI components
- Recharts for visualizations
- Axios for API calls
- CSS for styling (no CSS framework)

## Production Deployment

### Backend

For production, use a WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Frontend

Build the React app and serve with a web server:

```bash
cd frontend
npm run build
# Serve the build directory with nginx, Apache, or similar
```

## Screenshots

Screenshots demonstrating dashboard functionality should be placed in:
```
reports/screenshots/
```

## API Documentation

### Price Data Endpoint

**GET** `/api/price-data`

Query Parameters:
- `start_date` (optional): Start date in YYYY-MM-DD format
- `end_date` (optional): End date in YYYY-MM-DD format
- `frequency` (optional): 'D' (daily), 'W' (weekly), 'M' (monthly)

Response:
```json
{
  "dates": ["2000-01-01", "2000-01-02", ...],
  "prices": [25.50, 25.75, ...]
}
```

### Events Endpoint

**GET** `/api/events`

Query Parameters:
- `start_date` (optional): Start date filter
- `end_date` (optional): End date filter
- `event_type` (optional): Filter by event type
- `impact_type` (optional): Filter by impact type

Response:
```json
[
  {
    "event_date": "2001-09-11",
    "event_type": "Terrorism",
    "event_description": "9/11 terrorist attacks",
    "impact_type": "Demand Shock",
    "severity": "High"
  },
  ...
]
```

## License

[Add license information here]
