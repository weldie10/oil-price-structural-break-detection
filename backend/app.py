"""
Flask backend API for Oil Price Structural Break Detection Dashboard.

This module provides REST API endpoints to serve:
- Historical price data
- Change point results
- Event correlation data
- Performance metrics
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from data_loader import load_event_data as load_event_data_from_file, preprocess_data
from event_integration import align_events_with_prices, calculate_event_impact_statistics

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Configuration
DATA_DIR = Path(__file__).parent.parent / 'data'
PRICE_DATA_PATH = DATA_DIR / 'raw' / 'brent_prices.csv'
EVENT_DATA_PATH = DATA_DIR / 'raw' / 'oil_market_events.csv'

# Cache for loaded data
price_data_cache = None
event_data_cache = None


def load_price_data():
    """Load and cache price data."""
    global price_data_cache
    if price_data_cache is None:
        try:
            # Try loading from file
            if PRICE_DATA_PATH.exists():
                price_data_cache = pd.read_csv(PRICE_DATA_PATH, parse_dates=True, index_col=0)
                if not isinstance(price_data_cache.index, pd.DatetimeIndex):
                    price_data_cache.index = pd.to_datetime(price_data_cache.index)
                price_data_cache = preprocess_data(price_data_cache)
            else:
                # Return sample structure
                dates = pd.date_range(start='2000-01-01', end='2024-12-31', freq='D')
                price_data_cache = pd.DataFrame(index=dates, columns=['Price'])
                price_data_cache['Price'] = np.nan
        except Exception as e:
            print(f"Error loading price data: {e}")
            price_data_cache = pd.DataFrame()
    return price_data_cache


def load_event_data():
    """Load and cache event data."""
    global event_data_cache
    if event_data_cache is None:
        try:
            # Check if file exists
            if not EVENT_DATA_PATH.exists():
                print(f"Event data file not found: {EVENT_DATA_PATH}")
                print(f"Current working directory: {Path.cwd()}")
                print(f"Backend directory: {Path(__file__).parent}")
                event_data_cache = pd.DataFrame()
            else:
                # Try loading with the imported function
                event_data_cache = load_event_data_from_file(str(EVENT_DATA_PATH))
                print(f"✓ Loaded {len(event_data_cache)} events from {EVENT_DATA_PATH}")
                if not event_data_cache.empty:
                    print(f"  Event date range: {event_data_cache['event_date'].min()} to {event_data_cache['event_date'].max()}")
        except Exception as e:
            print(f"✗ Error loading event data: {e}")
            import traceback
            traceback.print_exc()
            # Try direct pandas load as fallback with proper quoting
            try:
                print("Attempting direct pandas load with quoting...")
                try:
                    event_data_cache = pd.read_csv(
                        EVENT_DATA_PATH, 
                        parse_dates=['event_date'],
                        quotechar='"',
                        quoting=1,  # QUOTE_ALL
                        on_bad_lines='skip'  # pandas >= 1.3
                    )
                except TypeError:
                    # Fallback for older pandas versions
                    event_data_cache = pd.read_csv(
                        EVENT_DATA_PATH, 
                        parse_dates=['event_date'],
                        quotechar='"',
                        quoting=1,
                        error_bad_lines=False,
                        warn_bad_lines=True
                    )
                print(f"✓ Loaded {len(event_data_cache)} events using direct pandas load")
            except Exception as e2:
                print(f"✗ Direct pandas load also failed: {e2}")
                import traceback
                traceback.print_exc()
                event_data_cache = pd.DataFrame()
    return event_data_cache


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy', 
        'message': 'API is running',
        'event_file_exists': EVENT_DATA_PATH.exists(),
        'event_file_path': str(EVENT_DATA_PATH),
        'price_file_exists': PRICE_DATA_PATH.exists()
    })


@app.route('/api/price-data', methods=['GET'])
def get_price_data():
    """
    Get historical price data.
    
    Query parameters:
    - start_date: Start date (YYYY-MM-DD)
    - end_date: End date (YYYY-MM-DD)
    - frequency: 'D' (daily), 'W' (weekly), 'M' (monthly)
    """
    try:
        df = load_price_data()
        
        if df.empty:
            return jsonify({'error': 'No price data available'}), 404
        
        # Get query parameters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        frequency = request.args.get('frequency', 'D')
        
        # Filter by date range
        if start_date:
            df = df[df.index >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df.index <= pd.to_datetime(end_date)]
        
        # Resample if needed
        if frequency == 'W':
            df = df.resample('W').last()
        elif frequency == 'M':
            df = df.resample('M').last()
        
        # Convert to JSON format
        result = {
            'dates': df.index.strftime('%Y-%m-%d').tolist(),
            'prices': df['Price'].fillna(0).tolist() if 'Price' in df.columns else []
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/events', methods=['GET'])
def get_events():
    """
    Get event data.
    
    Query parameters:
    - start_date: Start date (YYYY-MM-DD)
    - end_date: End date (YYYY-MM-DD)
    - event_type: Filter by event type
    - impact_type: Filter by impact type
    """
    try:
        df = load_event_data()
        
        # Check if file exists
        if not EVENT_DATA_PATH.exists():
            return jsonify({
                'error': f'Event data file not found at {EVENT_DATA_PATH}',
                'message': 'Please ensure the event data file exists'
            }), 404
        
        if df.empty:
            return jsonify({
                'error': 'No event data available',
                'message': 'Event data file is empty or could not be loaded'
            }), 404
        
        # Get query parameters
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        event_type = request.args.get('event_type')
        impact_type = request.args.get('impact_type')
        
        # Filter by date range
        if start_date:
            df = df[df['event_date'] >= pd.to_datetime(start_date)]
        if end_date:
            df = df[df['event_date'] <= pd.to_datetime(end_date)]
        
        # Filter by type
        if event_type and event_type != 'all':
            df = df[df['event_type'] == event_type]
        if impact_type and impact_type != 'all':
            df = df[df['impact_type'] == impact_type]
        
        # Convert to JSON format
        result = df.to_dict('records')
        
        # Convert datetime to string and handle NaN values
        for record in result:
            for key, value in record.items():
                if pd.isna(value):
                    record[key] = None
                elif key == 'event_date' and pd.notna(value):
                    if isinstance(value, pd.Timestamp):
                        record[key] = value.strftime('%Y-%m-%d')
                    elif isinstance(value, str):
                        # Already a string
                        pass
        
        # Return empty array if no events match filters (valid state)
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/change-points', methods=['GET'])
def get_change_points():
    """
    Get change point results.
    
    Returns detected change points from analysis.
    """
    try:
        # In a real implementation, this would load from saved model results
        # For now, return sample structure
        result = {
            'change_points': [
                {
                    'date': '2008-09-15',
                    'index': 1000,
                    'certainty': 0.95,
                    'mu_before': 0.0001,
                    'mu_after': -0.0002,
                    'price_before': 100.0,
                    'price_after': 50.0
                }
            ],
            'message': 'Change point data would be loaded from saved model results'
        }
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/event-correlation', methods=['GET'])
def get_event_correlation():
    """
    Get event correlation data.
    
    Returns price movements around events.
    """
    try:
        price_df = load_price_data()
        event_df = load_event_data()
        
        if price_df.empty or event_df.empty:
            return jsonify({'error': 'Required data not available'}), 404
        
        # Align events with prices
        if 'Price' in price_df.columns:
            events_with_prices = align_events_with_prices(
                price_df=price_df,
                event_df=event_df,
                price_column='Price',
                window_days=30
            )
            
            # Convert to JSON
            result = events_with_prices.to_dict('records')
            
            # Convert datetime and handle NaN
            for record in result:
                if 'event_date' in record and pd.notna(record['event_date']):
                    record['event_date'] = record['event_date'].strftime('%Y-%m-%d')
                # Replace NaN with None for JSON serialization
                for key, value in record.items():
                    if pd.isna(value):
                        record[key] = None
            
            return jsonify(result)
        else:
            return jsonify({'error': 'Price column not found'}), 404
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """
    Get summary statistics.
    
    Returns key indicators: volatility, average price changes, etc.
    """
    try:
        price_df = load_price_data()
        event_df = load_event_data()
        
        if price_df.empty:
            return jsonify({'error': 'No price data available'}), 404
        
        stats = {}
        
        if 'Price' in price_df.columns:
            # Price statistics
            stats['price'] = {
                'mean': float(price_df['Price'].mean()) if not price_df['Price'].isna().all() else 0,
                'std': float(price_df['Price'].std()) if not price_df['Price'].isna().all() else 0,
                'min': float(price_df['Price'].min()) if not price_df['Price'].isna().all() else 0,
                'max': float(price_df['Price'].max()) if not price_df['Price'].isna().all() else 0,
                'date_range': {
                    'start': price_df.index.min().strftime('%Y-%m-%d') if not price_df.empty else None,
                    'end': price_df.index.max().strftime('%Y-%m-%d') if not price_df.empty else None
                }
            }
            
            # Calculate returns and volatility
            returns = price_df['Price'].pct_change().dropna()
            if len(returns) > 0:
                stats['volatility'] = {
                    'daily': float(returns.std()),
                    'annualized': float(returns.std() * np.sqrt(252))
                }
        
        # Event statistics
        if not event_df.empty:
            stats['events'] = {
                'total': len(event_df),
                'by_type': event_df['event_type'].value_counts().to_dict() if 'event_type' in event_df.columns else {},
                'by_impact': event_df['impact_type'].value_counts().to_dict() if 'impact_type' in event_df.columns else {},
                'by_severity': event_df['severity'].value_counts().to_dict() if 'severity' in event_df.columns else {}
            }
        
        return jsonify(stats)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/event-impact/<event_id>', methods=['GET'])
def get_event_impact(event_id):
    """
    Get detailed impact analysis for a specific event.
    
    Parameters:
    - event_id: Index of the event in the dataset
    """
    try:
        price_df = load_price_data()
        event_df = load_event_data()
        
        if event_df.empty:
            return jsonify({'error': 'No event data available'}), 404
        
        event_id = int(event_id)
        if event_id >= len(event_df) or event_id < 0:
            return jsonify({'error': 'Invalid event ID'}), 404
        
        event = event_df.iloc[event_id]
        event_date = pd.to_datetime(event['event_date'])
        
        # Get price data around event
        window_days = int(request.args.get('window_days', 30))
        window_start = event_date - pd.Timedelta(days=window_days)
        window_end = event_date + pd.Timedelta(days=window_days)
        
        if 'Price' in price_df.columns:
            window_prices = price_df[
                (price_df.index >= window_start) & (price_df.index <= window_end)
            ]['Price']
            
            result = {
                'event': event.to_dict(),
                'event_date': event_date.strftime('%Y-%m-%d'),
                'price_data': {
                    'dates': window_prices.index.strftime('%Y-%m-%d').tolist(),
                    'prices': window_prices.fillna(0).tolist()
                },
                'window_days': window_days
            }
            
            # Convert event date to string
            if 'event_date' in result['event']:
                result['event']['event_date'] = event_date.strftime('%Y-%m-%d')
            
            return jsonify(result)
        else:
            return jsonify({'error': 'Price data not available'}), 404
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
