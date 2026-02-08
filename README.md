# Oil Price Structural Break Detection

A modular Python project for detecting structural breaks in Brent crude oil price time series data using statistical and Bayesian change point detection methods.

## Features

- **Time Series Analysis**: Comprehensive EDA including trend, stationarity, and volatility analysis
- **Change Point Detection**: Statistical methods to identify structural breaks in oil prices
- **Event Integration**: Correlate detected breaks with major market events (OPEC decisions, geopolitical events, economic shocks)
- **Modular Design**: Well-structured codebase with separation of concerns and comprehensive error handling
- **Reproducible Analysis**: Jupyter notebooks documenting the complete workflow

## Project Structure

```
oil-price-structural-break-detection/
├── data/
│   ├── raw/              # Raw data files (price data, event data)
│   └── processed/        # Processed data files
├── notebooks/            # Jupyter notebooks for analysis
│   └── TASK1_Foundation_Analysis.ipynb
├── src/                  # Source code modules
│   ├── data_loader.py    # Data loading and validation
│   ├── eda.py            # Exploratory data analysis
│   ├── event_integration.py  # Event data integration
│   └── main.py           # Main analysis pipeline
├── tests/                # Unit and integration tests
├── reports/              # Generated reports and visualizations
│   └── figures/          # Figures and plots
├── models/               # Trained models
├── requirements.txt      # Python dependencies
├── MODULAR_DESIGN.md     # Architecture documentation
└── README.md             # This file
```

## Setup

1. **Clone the repository** (if applicable)

2. **Create a virtual environment**:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
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

## Architecture

The project follows a modular design with:
- **Custom exception classes** for domain-specific error handling
- **Input validation** at all function entry points
- **Comprehensive logging** for debugging and monitoring
- **Type hints** throughout for better code clarity

See `MODULAR_DESIGN.md` for detailed architecture documentation.

## Requirements

- Python 3.8+
- See `requirements.txt` for full dependency list

## License

[Add license information here]
