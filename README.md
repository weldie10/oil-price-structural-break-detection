# Oil Price Structural Break Detection

A comprehensive Python project for detecting structural breaks in Brent crude oil price time series data using statistical and Bayesian change point detection methods, with an interactive web dashboard.

## Features

- **Time Series Analysis**: Comprehensive EDA including trend, stationarity, and volatility analysis
- **Bayesian Change Point Detection**: PyMC-based models to identify structural breaks with uncertainty quantification
- **Event Integration**: Correlate detected breaks with major market events (OPEC decisions, geopolitical events, economic shocks)
- **Interactive Dashboard**: Flask + React web application with filtering, visualization, and event highlighting
- **Modular Design**: Well-structured codebase with separation of concerns and comprehensive error handling
- **Reproducible Analysis**: Jupyter notebooks documenting the complete workflow

## Project Structure

```
oil-price-structural-break-detection/
├── backend/                 # Flask API server
│   ├── app.py              # API endpoints
│   ├── utils.py            # Backend utilities (validation, error handling)
│   └── README.md           # API documentation
├── frontend/               # React dashboard
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── services/       # API service layer
│   │   └── utils/          # Frontend utilities
│   ├── package.json
│   └── README.md           # Frontend documentation
├── data/
│   ├── raw/                # Raw data files (price data, event data)
│   └── processed/          # Processed data files
├── notebooks/              # Jupyter notebooks for analysis
│   ├── TASK1_Foundation_Analysis.ipynb
│   └── TASK2_ChangePoint_Modeling.ipynb
├── src/                    # Python source code modules
│   ├── data_loader.py      # Data loading and validation
│   ├── eda.py              # Exploratory data analysis
│   ├── event_integration.py # Event data integration
│   └── main.py             # Main analysis pipeline
├── tests/                  # Unit and integration tests
├── reports/                # Generated reports and visualizations
│   ├── figures/            # Figures and plots
│   └── screenshots/        # Dashboard screenshots
├── models/                 # Trained models
├── requirements.txt        # Python dependencies
├── MODULAR_DESIGN.md       # Architecture documentation
└── README.md               # This file
```

## Quick Start

### 1. Backend Setup

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the Flask API server
cd backend
python app.py
```

The API will be available at `http://localhost:5000`

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm start
```

The dashboard will open at `http://localhost:3000`

## Usage

### Python Analysis Pipeline

```python
from src.main import run_analysis_pipeline

results = run_analysis_pipeline(
    price_file_path="data/raw/brent_prices.csv",
    event_file_path="data/raw/oil_market_events.csv",
    start_date="2000-01-01",
    end_date="2024-12-31"
)
```

### Using Individual Modules

```python
from src.data_loader import load_oil_price_data, validate_data, preprocess_data
from src.eda import trend_analysis, test_stationarity, volatility_analysis
from src.event_integration import load_event_data, align_events_with_prices

# Load and validate data
price_df = load_oil_price_data("data/raw/brent_prices.csv")
validation_report = validate_data(price_df)
price_df_clean = preprocess_data(price_df)

# Perform analysis
trend_results = trend_analysis(price_df_clean)
stationarity_results = test_stationarity(price_df_clean['price'])
volatility_results = volatility_analysis(price_df_clean)

# Integrate events
events_df = load_event_data()
events_with_prices = align_events_with_prices(price_df_clean, events_df)
```

### Jupyter Notebooks

- `notebooks/TASK1_Foundation_Analysis.ipynb` - Foundation analysis and EDA
- `notebooks/TASK2_ChangePoint_Modeling.ipynb` - Bayesian change point detection

## Dashboard Features

### Interactive Features
- **Date Range Filters**: Filter price data by start and end dates
- **Event Filters**: Filter events by type, impact type, and severity
- **Visual Event Highlighting**: Events marked on charts with color coding
- **Real-time Statistics**: Price statistics update based on selected filters
- **Responsive Design**: Works on desktop, tablet, and mobile devices

### API Endpoints

- `GET /api/health` - Health check
- `GET /api/price-data` - Price data with date filtering
- `GET /api/events` - Event data with filtering
- `GET /api/event-filters` - Available filter options
- `GET /api/statistics` - Price statistics

See `backend/README.md` for detailed API documentation.

## Code Quality & Best Practices

The codebase follows industry best practices:

### Backend
- **Utility Modules**: Reusable validation and error handling functions (`backend/utils.py`)
- **Error Handling**: Comprehensive error handling with standardized responses
- **Input Validation**: All API endpoints validate inputs before processing
- **Status Codes**: Appropriate HTTP status codes (200, 400, 500, 503)
- **Logging**: Comprehensive logging for debugging and monitoring

### Frontend
- **Utility Modules**: Reusable validation, error handling, and data transformation (`frontend/src/utils/`)
- **Input Validation**: Real-time validation with user feedback
- **Error Handling**: User-friendly error messages and graceful error handling
- **Accessibility**: ARIA attributes and semantic HTML
- **Responsive Design**: CSS Grid/Flexbox with media queries

### Naming Conventions
- **Backend**: `snake_case` for functions, `PascalCase` for classes
- **Frontend**: `camelCase` for functions, `PascalCase` for components

## Architecture

The project follows a modular design with:
- **Custom exception classes** for domain-specific error handling
- **Input validation** at all function entry points
- **Comprehensive logging** for debugging and monitoring
- **Type hints** throughout for better code clarity
- **Separation of concerns** between backend, frontend, and analysis modules

See `MODULAR_DESIGN.md` for detailed architecture documentation.

## Requirements

- **Python**: 3.8+
- **Node.js**: 16+
- **npm**: Latest stable version

See `requirements.txt` for Python dependencies and `frontend/package.json` for frontend dependencies.

## Development

### Running Tests

```bash
# Python tests
pytest

# Frontend tests
cd frontend
npm test
```

### Building for Production

```bash
# Frontend production build
cd frontend
npm run build
```

### Code Quality

- All utility functions have comprehensive docstrings
- Type hints used throughout Python code
- JSDoc comments in JavaScript code
- Consistent error handling patterns
- Input validation at all entry points

## Data Files

Place your data files in `data/raw/`:
- `brent_prices.csv` - Price data with date index
- `oil_market_events.csv` - Event data with event_date column

If data files are not found, the API will generate sample data for demonstration.

## Screenshots

Dashboard screenshots are located in `reports/screenshots/`. See `reports/screenshots/README.md` for instructions on taking screenshots.

## License

[Add license information here]

## Contributing

[Add contributing guidelines here]
