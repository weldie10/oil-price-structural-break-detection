# Oil Price Structural Break Detection

A modular Python project for detecting structural breaks in Brent crude oil price time series data using statistical and Bayesian change point detection methods. Includes an interactive dashboard for visualizing analysis results.

## Features

- **Time Series Analysis**: Comprehensive EDA including trend, stationarity, and volatility analysis
- **Change Point Detection**: Bayesian methods (PyMC) to identify structural breaks in oil prices
- **Event Integration**: Correlate detected breaks with major market events (OPEC decisions, geopolitical events, economic shocks)
- **Interactive Dashboard**: React-based web application with Flask backend for exploring results
- **Modular Design**: Well-structured codebase with separation of concerns and comprehensive error handling
- **Reproducible Analysis**: Jupyter notebooks documenting the complete workflow

## Project Structure

```
oil-price-structural-break-detection/
├── backend/              # Flask REST API
│   ├── app.py           # API server
│   └── requirements.txt  # Backend dependencies
├── frontend/            # React dashboard application
│   ├── src/             # React components
│   ├── public/          # Static files
│   └── package.json     # Frontend dependencies
├── data/
│   ├── raw/             # Raw data files (price data, event data)
│   └── processed/       # Processed data files
├── notebooks/           # Jupyter notebooks for analysis
│   └── TASK1_Foundation_Analysis.ipynb
├── src/                 # Source code modules
│   ├── data_loader.py   # Data loading and validation
│   ├── eda.py           # Exploratory data analysis
│   ├── event_integration.py  # Event data integration
│   └── main.py          # Main analysis pipeline
├── tests/               # Unit and integration tests
├── reports/             # Generated reports and visualizations
│   ├── figures/         # Figures and plots
│   ├── COMMUNICATION_CHANNELS.md
│   └── TASK1_COMPLETION_SUMMARY.md
├── models/              # Trained models
├── requirements.txt     # Python dependencies
├── MODULAR_DESIGN.md     # Architecture documentation
├── DASHBOARD_README.md   # Dashboard setup instructions
└── README.md             # This file
```

## Setup

### Prerequisites

- Python 3.8+
- Node.js 16+ and npm (for dashboard)
- Git

### Installation

1. **Clone the repository** (if applicable)

2. **Create a virtual environment**:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install Python dependencies**:
```bash
pip install -r requirements.txt
```

4. **Install frontend dependencies** (for dashboard):
```bash
cd frontend
npm install
cd ..
```

## Usage

### Running the Analysis Pipeline

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

Open `notebooks/TASK1_Foundation_Analysis.ipynb` for a complete walkthrough of the analysis workflow.

### Interactive Dashboard

The project includes an interactive web dashboard for visualizing analysis results.

**Quick Start**:
```bash
# Terminal 1: Start Flask backend
cd backend
python app.py

# Terminal 2: Start React frontend
cd frontend
npm start
```

Access the dashboard at `http://localhost:3000`

**Features**:
- Interactive price charts with event markers
- Filter by date range, event type, and impact type
- Event highlight functionality
- Key statistics and indicators
- Responsive design for all devices

See `DASHBOARD_README.md` for detailed setup and API documentation.

## Project Tasks

This project implements three main tasks:

### Task 1: Foundation Analysis
- Data analysis workflow documentation
- Event data research and compilation (22 events)
- Assumptions and limitations documentation
- Communication channels for stakeholders
- Time series properties analysis (trend, stationarity, volatility)
- Change point model understanding

**Deliverables**: See `notebooks/TASK1_Foundation_Analysis.ipynb` and `reports/`

### Task 2: Change Point Modeling
- Bayesian change point detection using PyMC
- MCMC sampling and convergence diagnostics
- Change point identification and impact quantification
- Event association and correlation analysis

**Deliverables**: See `notebooks/TASK2_ChangePoint_Modeling.ipynb` (to be created)

### Task 3: Interactive Dashboard
- Flask REST API backend
- React frontend with interactive visualizations
- Event highlight and filtering functionality
- Responsive design for all devices

**Deliverables**: See `backend/`, `frontend/`, and `DASHBOARD_README.md`

## Architecture

The project follows a modular design with:
- **Custom exception classes** for domain-specific error handling
- **Input validation** at all function entry points
- **Comprehensive logging** for debugging and monitoring
- **Type hints** throughout for better code clarity

See `MODULAR_DESIGN.md` for detailed architecture documentation.

## Documentation

- **README.md**: This file - project overview and quick start
- **DASHBOARD_README.md**: Detailed dashboard setup and API documentation
- **MODULAR_DESIGN.md**: Architecture and design patterns
- **reports/COMMUNICATION_CHANNELS.md**: Stakeholder communication strategies
- **reports/TASK1_COMPLETION_SUMMARY.md**: Task 1 completion verification

## Requirements

- Python 3.8+
- Node.js 16+ and npm (for dashboard)
- See `requirements.txt` for full Python dependency list
- See `frontend/package.json` for frontend dependencies

## License

[Add license information here]
