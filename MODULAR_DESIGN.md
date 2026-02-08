# Modular Design Documentation

## Overview

This project demonstrates a **modular design** with clear separation of concerns, comprehensive error handling, and well-structured code organization.

## Module Structure

### 1. `src/data_loader.py` - Data Loading Module

**Purpose**: Handles all data loading, validation, and preprocessing operations.

**Key Features**:
- Custom exception classes (`DataLoadingError`, `DataValidationError`)
- Input validation for all parameters
- Comprehensive error handling with try-except blocks
- Logging for debugging and monitoring
- Type hints for clear function signatures

**Functions**:
- `load_oil_price_data()`: Loads price data from CSV with validation
- `validate_data()`: Validates data quality and returns report
- `preprocess_data()`: Handles missing values with multiple strategies
- `load_event_data()`: Loads event data with error checking

**Error Handling Examples**:
```python
# Validates file existence
if not file_path_obj.exists():
    raise DataLoadingError(f"File not found: {file_path}")

# Validates DataFrame is not empty
if df.empty:
    raise DataLoadingError("Loaded DataFrame is empty")

# Handles parsing errors
except pd.errors.ParserError as e:
    raise DataLoadingError(f"Failed to parse CSV file: {e}")
```

### 2. `src/eda.py` - Exploratory Data Analysis Module

**Purpose**: Performs time series analysis including trend, stationarity, and volatility analysis.

**Key Features**:
- Custom exception class (`EDAError`)
- Input validation (checking for empty data, invalid parameters)
- Graceful error handling for statistical tests
- Logging for analysis progress
- Type hints and comprehensive docstrings

**Functions**:
- `descriptive_statistics()`: Calculates summary statistics
- `trend_analysis()`: Analyzes trends with moving averages and decomposition
- `test_stationarity()`: Performs ADF and KPSS tests
- `volatility_analysis()`: Analyzes volatility patterns and ARCH effects
- `autocorrelation_analysis()`: Calculates ACF and PACF

**Error Handling Examples**:
```python
# Validates input data
if df is None or df.empty:
    raise EDAError("DataFrame is None or empty")

# Validates parameters
if window <= 0:
    raise ValueError(f"Window must be positive, got {window}")

# Handles insufficient data gracefully
if len(series_clean) < 10:
    raise EDAError(f"Insufficient data: {len(series_clean)} observations")
```

### 3. `src/event_integration.py` - Event Integration Module

**Purpose**: Integrates event data with price data and calculates impact metrics.

**Key Features**:
- Custom exception class (`EventIntegrationError`)
- Validates DataFrame structure and required columns
- Handles missing or invalid event dates gracefully
- Logging for alignment progress
- Type hints and error messages

**Functions**:
- `align_events_with_prices()`: Aligns events with price data and calculates impacts
- `categorize_events()`: Groups events by type and impact
- `calculate_event_impact_statistics()`: Computes summary statistics

**Error Handling Examples**:
```python
# Validates required columns exist
if price_column not in price_df.columns:
    raise EventIntegrationError(f"Price column '{price_column}' not found")

# Validates DataFrame structure
if not isinstance(price_df.index, pd.DatetimeIndex):
    raise EventIntegrationError("Price DataFrame must have DatetimeIndex")

# Handles missing data gracefully
if len(window_prices) == 0:
    logger.warning(f"No price data found for event at {event_date}")
    continue
```

### 4. `src/main.py` - Main Pipeline Module

**Purpose**: Demonstrates modular design by orchestrating all modules together.

**Key Features**:
- Complete analysis pipeline
- Error handling at each step
- Logging throughout the process
- Demonstrates how modules work together
- Clear structure showing separation of concerns

**Pipeline Steps**:
1. Load price data (with error handling)
2. Validate data quality
3. Preprocess data
4. Perform EDA (trend, stationarity, volatility)
5. Load and integrate event data
6. Calculate event impacts

## Design Principles

### 1. Separation of Concerns
Each module has a single, well-defined responsibility:
- **Data Loading**: Only handles data I/O and validation
- **EDA**: Only performs statistical analysis
- **Event Integration**: Only handles event-price alignment
- **Main**: Only orchestrates the pipeline

### 2. Error Handling
- **Custom Exceptions**: Each module defines its own exception classes
- **Input Validation**: All functions validate inputs before processing
- **Graceful Degradation**: Errors are caught and logged, allowing pipeline to continue where possible
- **Clear Error Messages**: Exceptions include descriptive error messages

### 3. Logging
- All modules use Python's `logging` module
- Log levels: INFO for normal operations, WARNING for recoverable issues, ERROR for failures
- Consistent log format across modules

### 4. Type Hints
- All functions include type hints for parameters and return values
- Improves code readability and IDE support
- Enables static type checking

### 5. Documentation
- Comprehensive docstrings for all functions
- Clear parameter descriptions
- Return value documentation
- Exception documentation

## Usage Example

```python
from src.data_loader import load_oil_price_data, validate_data, preprocess_data
from src.eda import trend_analysis, test_stationarity, volatility_analysis
from src.event_integration import load_event_data, align_events_with_prices

# Load and validate data
try:
    price_df = load_oil_price_data("data/raw/brent_prices.csv")
    validation_report = validate_data(price_df)
    price_df_clean = preprocess_data(price_df)
except DataLoadingError as e:
    print(f"Error loading data: {e}")
    exit(1)

# Perform analysis
try:
    trend_results = trend_analysis(price_df_clean)
    stationarity_results = test_stationarity(price_df_clean['price'])
    volatility_results = volatility_analysis(price_df_clean)
except EDAError as e:
    print(f"Error in analysis: {e}")
    exit(1)

# Integrate events
try:
    events_df = load_event_data()
    events_with_prices = align_events_with_prices(price_df_clean, events_df)
except EventIntegrationError as e:
    print(f"Error integrating events: {e}")
    exit(1)
```

## Running the Pipeline

```bash
# Run the main pipeline
python src/main.py

# Or import and use programmatically
from src.main import run_analysis_pipeline

results = run_analysis_pipeline(
    price_file_path="data/raw/brent_prices.csv",
    event_file_path="data/raw/oil_market_events.csv"
)
```

## Benefits of Modular Design

1. **Maintainability**: Each module can be modified independently
2. **Testability**: Each module can be tested in isolation
3. **Reusability**: Modules can be used in different contexts
4. **Readability**: Clear structure makes code easy to understand
5. **Error Handling**: Centralized error handling makes debugging easier
6. **Scalability**: Easy to add new modules or extend existing ones

## Error Handling Strategy

1. **Input Validation**: Validate all inputs at function entry
2. **Try-Except Blocks**: Wrap risky operations in try-except
3. **Custom Exceptions**: Use domain-specific exceptions
4. **Logging**: Log all errors with appropriate levels
5. **Graceful Degradation**: Continue processing where possible
6. **Clear Messages**: Provide descriptive error messages

## Testing the Modular Design

Each module can be tested independently:

```python
# Test data loading
def test_load_data():
    try:
        df = load_oil_price_data("test_data.csv")
        assert not df.empty
    except DataLoadingError:
        # Handle expected errors
        pass

# Test EDA
def test_trend_analysis():
    try:
        results = trend_analysis(test_df)
        assert "price_linear_trend" in results
    except EDAError:
        # Handle expected errors
        pass
```

## Conclusion

This modular design demonstrates:
- ✅ Clear separation of concerns
- ✅ Comprehensive error handling
- ✅ Well-structured code organization
- ✅ Reusable and maintainable components
- ✅ Professional software development practices
