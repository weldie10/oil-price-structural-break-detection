# Oil Price Dashboard - Backend API

Flask REST API for serving oil price data, events, and statistics to the React frontend.

## Features

- RESTful API endpoints for price data, events, and statistics
- Date range filtering
- Event filtering by type, impact type, and severity
- CORS enabled for frontend integration
- Automatic data loading and caching
- Sample data generation if data files are not found

## Setup

### Prerequisites

- Python 3.8+
- Virtual environment (recommended)

### Installation

1. Navigate to the project root directory

2. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Start the Flask server:
```bash
cd backend
python app.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### Health Check
```
GET /api/health
```
Returns API health status and data loading status.

### Price Data
```
GET /api/price-data?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD
```
Returns price data with optional date range filtering.

**Query Parameters:**
- `start_date` (optional): Start date in YYYY-MM-DD format
- `end_date` (optional): End date in YYYY-MM-DD format

**Response:**
```json
{
  "dates": ["2000-01-01", ...],
  "prices": [20.5, ...],
  "min_date": "2000-01-01",
  "max_date": "2024-12-31",
  "count": 9125
}
```

### Events
```
GET /api/events?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD&event_type=TYPE&impact_type=TYPE&severity=SEVERITY
```
Returns event data with optional filtering.

**Query Parameters:**
- `start_date` (optional): Start date filter
- `end_date` (optional): End date filter
- `event_type` (optional): Filter by event type
- `impact_type` (optional): Filter by impact type
- `severity` (optional): Filter by severity

**Response:**
```json
{
  "events": [
    {
      "event_date": "2008-09-15",
      "event_type": "Economic",
      "event_description": "Lehman Brothers collapse",
      "impact_type": "Demand Shock",
      "severity": "Very High"
    },
    ...
  ],
  "count": 4
}
```

### Event Filters
```
GET /api/event-filters
```
Returns available filter options for events.

**Response:**
```json
{
  "event_types": ["OPEC", "Geopolitical", "Economic", ...],
  "impact_types": ["Supply Shock", "Demand Shock", ...],
  "severities": ["Very High", "High", "Medium"]
}
```

### Statistics
```
GET /api/statistics?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD
```
Returns price statistics for the specified date range.

**Query Parameters:**
- `start_date` (optional): Start date filter
- `end_date` (optional): End date filter

**Response:**
```json
{
  "mean": 65.5,
  "median": 62.3,
  "std": 25.8,
  "min": 20.1,
  "max": 140.2,
  "count": 9125
}
```

## Data Files

The API looks for data files in the following locations (in order):
1. `data/raw/brent_prices.csv` - Price data
2. `data/raw/oil_market_events.csv` - Event data

If data files are not found, the API will generate sample data for demonstration purposes.

## Configuration

- **Port**: Default 5000 (change in `app.py` if needed)
- **CORS**: Enabled for all origins (configure in production)
- **Debug Mode**: Enabled by default (disable in production)

## Error Handling

All endpoints return appropriate HTTP status codes:
- `200`: Success
- `400`: Bad request (invalid parameters)
- `500`: Server error

Error responses include an error message:
```json
{
  "error": "Error message here"
}
```
