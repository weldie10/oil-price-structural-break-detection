"""
Flask API backend for Oil Price Structural Break Detection Dashboard.

This module provides REST API endpoints for:
- Price data retrieval with date filtering
- Event data retrieval with filtering
- Change point data retrieval
- Data aggregation and statistics
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path
import sys
import logging

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from data_loader import load_oil_price_data, load_event_data, DataLoadingError
from event_integration import align_events_with_prices

# Import backend utilities
from utils import (
    ValidationError,
    APIError,
    validate_date_string,
    validate_date_range,
    validate_filter_value,
    create_error_response,
    create_success_response,
    apply_date_filter_to_dataframe,
    convert_dataframe_to_json_serializable,
    validate_dataframe_not_empty,
    get_query_parameter
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Global data cache (in production, use a proper cache or database)
_data_cache = {}


def load_data():
    """Load and cache data on startup."""
    global _data_cache
    
    try:
        # Try to load price data
        price_paths = [
            "data/raw/brent_prices.csv",
            "../data/raw/brent_prices.csv",
            str(Path(__file__).parent.parent / "data/raw/brent_prices.csv")
        ]
        
        price_df = None
        for path in price_paths:
            try:
                if Path(path).exists():
                    price_df = load_oil_price_data(path)
                    logger.info(f"Loaded price data from {path}")
                    break
            except Exception as e:
                logger.warning(f"Failed to load from {path}: {e}")
                continue
        
        # If no price data file, create sample data
        if price_df is None:
            logger.info("No price data file found, creating sample data")
            dates = pd.date_range(start='2000-01-01', end='2024-12-31', freq='D')
            np.random.seed(42)
            n = len(dates)
            price = np.zeros(n)
            price[0] = 20.0
            
            # Create realistic price series with multiple regimes
            for i in range(1, n):
                price[i] = price[i-1] * (1 + np.random.normal(0.0005, 0.015))
            
            price_df = pd.DataFrame({'price': price}, index=dates)
        
        _data_cache['price_data'] = price_df
        
        # Load event data
        event_paths = [
            "data/raw/oil_market_events.csv",
            "../data/raw/oil_market_events.csv",
            str(Path(__file__).parent.parent / "data/raw/oil_market_events.csv")
        ]
        
        event_df = None
        for path in event_paths:
            try:
                if Path(path).exists():
                    event_df = load_event_data(path)
                    logger.info(f"Loaded event data from {path}")
                    break
            except Exception as e:
                logger.warning(f"Failed to load from {path}: {e}")
                continue
        
        if event_df is None:
            # Create sample event data
            logger.info("No event data file found, creating sample events")
            sample_events = [
                {'event_date': '2008-09-15', 'event_type': 'Economic', 'event_description': 'Lehman Brothers collapse', 'impact_type': 'Demand Shock', 'severity': 'Very High'},
                {'event_date': '2014-11-27', 'event_type': 'OPEC', 'event_description': 'OPEC decides not to cut production', 'impact_type': 'Supply Shock', 'severity': 'High'},
                {'event_date': '2020-03-09', 'event_type': 'Economic', 'event_description': 'COVID-19 pandemic impact', 'impact_type': 'Demand Shock', 'severity': 'Very High'},
                {'event_date': '2022-02-24', 'event_type': 'Geopolitical', 'event_description': 'Russia-Ukraine conflict', 'impact_type': 'Supply Shock', 'severity': 'Very High'},
            ]
            event_df = pd.DataFrame(sample_events)
            event_df['event_date'] = pd.to_datetime(event_df['event_date'])
        
        _data_cache['event_data'] = event_df
        
        # Align events with prices
        try:
            events_with_prices = align_events_with_prices(
                price_df, event_df, window_days=30
            )
            _data_cache['events_with_prices'] = events_with_prices
        except Exception as e:
            logger.warning(f"Failed to align events with prices: {e}")
            _data_cache['events_with_prices'] = event_df
        
        logger.info("Data loaded successfully")
        
    except Exception as e:
        logger.error(f"Error loading data: {e}")
        _data_cache = {}


# Load data on startup
load_data()


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'price_data_loaded': 'price_data' in _data_cache,
        'event_data_loaded': 'event_data' in _data_cache
    })


@app.route('/api/price-data', methods=['GET'])
def get_price_data():
    """
    Get price data with optional date range filtering.
    
    Query parameters:
    - start_date: Start date (YYYY-MM-DD)
    - end_date: End date (YYYY-MM-DD)
    
    Returns:
        JSON response with price data or error message
    """
    try:
        # Validate data availability
        if 'price_data' not in _data_cache:
            error_response, status_code = create_error_response(
                'Price data is not available. Please ensure data files are loaded.',
                status_code=503,
                error_type='DataUnavailableError'
            )
            return jsonify(error_response), status_code
        
        price_df = _data_cache['price_data'].copy()
        validate_dataframe_not_empty(price_df, "Price data")
        
        # Get and validate query parameters
        start_date = get_query_parameter(request, 'start_date', required=False)
        end_date = get_query_parameter(request, 'end_date', required=False)
        
        # Validate date range
        try:
            start_dt, end_dt = validate_date_range(start_date, end_date)
        except ValidationError as e:
            error_response, status_code = create_error_response(
                str(e),
                status_code=400,
                error_type='ValidationError'
            )
            return jsonify(error_response), status_code
        
        # Apply date filters using utility function
        try:
            filtered_df = apply_date_filter_to_dataframe(
                price_df,
                date_column='index',
                start_date=start_dt,
                end_date=end_dt
            )
            validate_dataframe_not_empty(filtered_df, "Filtered price data")
        except ValidationError as e:
            error_response, status_code = create_error_response(
                str(e),
                status_code=400,
                error_type='ValidationError'
            )
            return jsonify(error_response), status_code
        
        # Convert to JSON-serializable format
        result = {
            'dates': filtered_df.index.strftime('%Y-%m-%d').tolist(),
            'prices': [float(price) for price in filtered_df['price'].tolist()],
            'min_date': str(filtered_df.index.min()),
            'max_date': str(filtered_df.index.max()),
            'count': len(filtered_df)
        }
        
        success_response = create_success_response(result, status_code=200)
        return jsonify(success_response), 200
    
    except ValidationError as e:
        error_response, status_code = create_error_response(
            str(e),
            status_code=400,
            error_type='ValidationError'
        )
        return jsonify(error_response), status_code
    except Exception as e:
        logger.error(f"Unexpected error in get_price_data: {e}", exc_info=True)
        error_response, status_code = create_error_response(
            'An internal server error occurred while processing your request.',
            status_code=500,
            error_type='InternalServerError'
        )
        return jsonify(error_response), status_code


@app.route('/api/events', methods=['GET'])
def get_events():
    """
    Get event data with optional filtering.
    
    Query parameters:
    - start_date: Start date (YYYY-MM-DD)
    - end_date: End date (YYYY-MM-DD)
    - event_type: Filter by event type
    - impact_type: Filter by impact type
    - severity: Filter by severity
    
    Returns:
        JSON response with event data or error message
    """
    try:
        # Validate data availability
        if 'event_data' not in _data_cache:
            error_response, status_code = create_error_response(
                'Event data is not available. Please ensure data files are loaded.',
                status_code=503,
                error_type='DataUnavailableError'
            )
            return jsonify(error_response), status_code
        
        event_df = _data_cache['event_data'].copy()
        validate_dataframe_not_empty(event_df, "Event data")
        
        # Get and validate query parameters
        start_date = get_query_parameter(request, 'start_date', required=False)
        end_date = get_query_parameter(request, 'end_date', required=False)
        event_type = get_query_parameter(request, 'event_type', required=False)
        impact_type = get_query_parameter(request, 'impact_type', required=False)
        severity = get_query_parameter(request, 'severity', required=False)
        
        # Validate date range
        try:
            start_dt, end_dt = validate_date_range(start_date, end_date)
        except ValidationError as e:
            error_response, status_code = create_error_response(
                str(e),
                status_code=400,
                error_type='ValidationError'
            )
            return jsonify(error_response), status_code
        
        # Apply date filters using utility function
        try:
            filtered_df = apply_date_filter_to_dataframe(
                event_df,
                date_column='event_date',
                start_date=start_dt,
                end_date=end_dt
            )
        except ValidationError as e:
            error_response, status_code = create_error_response(
                str(e),
                status_code=400,
                error_type='ValidationError'
            )
            return jsonify(error_response), status_code
        
        # Get available filter values for validation
        available_event_types = []
        available_impact_types = []
        available_severities = []
        
        if 'event_type' in filtered_df.columns:
            available_event_types = filtered_df['event_type'].dropna().unique().tolist()
        if 'impact_type' in filtered_df.columns:
            available_impact_types = filtered_df['impact_type'].dropna().unique().tolist()
        if 'severity' in filtered_df.columns:
            available_severities = filtered_df['severity'].dropna().unique().tolist()
        
        # Validate and apply event type filter
        if event_type:
            try:
                validate_filter_value(event_type, available_event_types, 'event_type')
                filtered_df = filtered_df[filtered_df['event_type'] == event_type]
            except ValidationError as e:
                error_response, status_code = create_error_response(
                    str(e),
                    status_code=400,
                    error_type='ValidationError'
                )
                return jsonify(error_response), status_code
        
        # Validate and apply impact type filter
        if impact_type:
            try:
                validate_filter_value(impact_type, available_impact_types, 'impact_type')
                filtered_df = filtered_df[filtered_df['impact_type'] == impact_type]
            except ValidationError as e:
                error_response, status_code = create_error_response(
                    str(e),
                    status_code=400,
                    error_type='ValidationError'
                )
                return jsonify(error_response), status_code
        
        # Validate and apply severity filter
        if severity:
            try:
                validate_filter_value(severity, available_severities, 'severity')
                filtered_df = filtered_df[filtered_df['severity'] == severity]
            except ValidationError as e:
                error_response, status_code = create_error_response(
                    str(e),
                    status_code=400,
                    error_type='ValidationError'
                )
                return jsonify(error_response), status_code
        
        # Convert to JSON-serializable format using utility
        events_list = convert_dataframe_to_json_serializable(
            filtered_df,
            date_columns=['event_date']
        )
        
        result = {
            'events': events_list,
            'count': len(events_list)
        }
        
        success_response = create_success_response(result, status_code=200)
        return jsonify(success_response), 200
    
    except ValidationError as e:
        error_response, status_code = create_error_response(
            str(e),
            status_code=400,
            error_type='ValidationError'
        )
        return jsonify(error_response), status_code
    except Exception as e:
        logger.error(f"Unexpected error in get_events: {e}", exc_info=True)
        error_response, status_code = create_error_response(
            'An internal server error occurred while processing your request.',
            status_code=500,
            error_type='InternalServerError'
        )
        return jsonify(error_response), status_code


@app.route('/api/event-filters', methods=['GET'])
def get_event_filters():
    """
    Get available filter options for events.
    
    Returns:
        JSON response with available filter options or error message
    """
    try:
        # Validate data availability
        if 'event_data' not in _data_cache:
            error_response, status_code = create_error_response(
                'Event data is not available. Please ensure data files are loaded.',
                status_code=503,
                error_type='DataUnavailableError'
            )
            return jsonify(error_response), status_code
        
        event_df = _data_cache['event_data']
        validate_dataframe_not_empty(event_df, "Event data")
        
        # Extract available filter values
        filters = {}
        
        if 'event_type' in event_df.columns:
            filters['event_types'] = sorted(event_df['event_type'].dropna().unique().tolist())
        
        if 'impact_type' in event_df.columns:
            filters['impact_types'] = sorted(event_df['impact_type'].dropna().unique().tolist())
        
        if 'severity' in event_df.columns:
            filters['severities'] = sorted(event_df['severity'].dropna().unique().tolist())
        
        success_response = create_success_response(filters, status_code=200)
        return jsonify(success_response), 200
    
    except ValidationError as e:
        error_response, status_code = create_error_response(
            str(e),
            status_code=400,
            error_type='ValidationError'
        )
        return jsonify(error_response), status_code
    except Exception as e:
        logger.error(f"Unexpected error in get_event_filters: {e}", exc_info=True)
        error_response, status_code = create_error_response(
            'An internal server error occurred while processing your request.',
            status_code=500,
            error_type='InternalServerError'
        )
        return jsonify(error_response), status_code


@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """
    Get price statistics for a date range.
    
    Query parameters:
    - start_date: Start date (YYYY-MM-DD)
    - end_date: End date (YYYY-MM-DD)
    
    Returns:
        JSON response with price statistics or error message
    """
    try:
        # Validate data availability
        if 'price_data' not in _data_cache:
            error_response, status_code = create_error_response(
                'Price data is not available. Please ensure data files are loaded.',
                status_code=503,
                error_type='DataUnavailableError'
            )
            return jsonify(error_response), status_code
        
        price_df = _data_cache['price_data'].copy()
        validate_dataframe_not_empty(price_df, "Price data")
        
        # Get and validate query parameters
        start_date = get_query_parameter(request, 'start_date', required=False)
        end_date = get_query_parameter(request, 'end_date', required=False)
        
        # Validate date range
        try:
            start_dt, end_dt = validate_date_range(start_date, end_date)
        except ValidationError as e:
            error_response, status_code = create_error_response(
                str(e),
                status_code=400,
                error_type='ValidationError'
            )
            return jsonify(error_response), status_code
        
        # Apply date filters using utility function
        try:
            filtered_df = apply_date_filter_to_dataframe(
                price_df,
                date_column='index',
                start_date=start_dt,
                end_date=end_dt
            )
            validate_dataframe_not_empty(filtered_df, "Filtered price data")
        except ValidationError as e:
            error_response, status_code = create_error_response(
                str(e),
                status_code=400,
                error_type='ValidationError'
            )
            return jsonify(error_response), status_code
        
        # Calculate statistics with error handling
        try:
            price_series = filtered_df['price']
            stats = {
                'mean': float(price_series.mean()),
                'median': float(price_series.median()),
                'std': float(price_series.std()),
                'min': float(price_series.min()),
                'max': float(price_series.max()),
                'count': len(filtered_df)
            }
        except Exception as e:
            logger.error(f"Error calculating statistics: {e}")
            error_response, status_code = create_error_response(
                'Failed to calculate statistics. Please check your date range.',
                status_code=500,
                error_type='CalculationError'
            )
            return jsonify(error_response), status_code
        
        success_response = create_success_response(stats, status_code=200)
        return jsonify(success_response), 200
    
    except ValidationError as e:
        error_response, status_code = create_error_response(
            str(e),
            status_code=400,
            error_type='ValidationError'
        )
        return jsonify(error_response), status_code
    except Exception as e:
        logger.error(f"Unexpected error in get_statistics: {e}", exc_info=True)
        error_response, status_code = create_error_response(
            'An internal server error occurred while processing your request.',
            status_code=500,
            error_type='InternalServerError'
        )
        return jsonify(error_response), status_code


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
