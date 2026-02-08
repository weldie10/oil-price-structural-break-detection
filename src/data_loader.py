"""
Data loading and validation module for Brent crude oil price analysis.

This module provides functions for loading, validating, and preprocessing
oil price time series data with comprehensive error handling.
"""

import pandas as pd
import numpy as np
from typing import Optional, Tuple, Dict
import warnings
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DataLoadingError(Exception):
    """Custom exception for data loading errors."""
    pass


class DataValidationError(Exception):
    """Custom exception for data validation errors."""
    pass


def load_oil_price_data(
    file_path: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    frequency: str = "D"
) -> pd.DataFrame:
    """
    Load Brent crude oil price data with error handling and validation.
    
    Parameters:
    -----------
    file_path : str, optional
        Path to CSV file containing oil price data.
        If None, will attempt to fetch from online source.
    start_date : str, optional
        Start date in 'YYYY-MM-DD' format
    end_date : str, optional
        End date in 'YYYY-MM-DD' format
    frequency : str
        Data frequency ('D' for daily, 'W' for weekly, 'M' for monthly)
    
    Returns:
    --------
    pd.DataFrame
        DataFrame with date index and price column(s)
    
    Raises:
    -------
    DataLoadingError
        If file cannot be loaded or data is invalid
    ValueError
        If parameters are invalid
    """
    # Input validation
    if frequency not in ["D", "W", "M"]:
        raise ValueError(f"Invalid frequency: {frequency}. Must be 'D', 'W', or 'M'")
    
    if file_path is None:
        raise DataLoadingError("No file path provided. Please provide a file_path or implement online data source.")
    
    # Validate file exists
    file_path_obj = Path(file_path)
    if not file_path_obj.exists():
        raise DataLoadingError(f"File not found: {file_path}")
    
    try:
        # Load data
        logger.info(f"Loading data from {file_path}")
        df = pd.read_csv(file_path, parse_dates=True, index_col=0)
        
        if df.empty:
            raise DataLoadingError("Loaded DataFrame is empty")
        
        # Ensure date index
        if not isinstance(df.index, pd.DatetimeIndex):
            try:
                df.index = pd.to_datetime(df.index)
            except Exception as e:
                raise DataLoadingError(f"Failed to convert index to datetime: {e}")
        
        # Filter by date range
        if start_date:
            try:
                start_dt = pd.to_datetime(start_date)
                df = df[df.index >= start_dt]
                logger.info(f"Filtered data from {start_date}")
            except Exception as e:
                raise DataLoadingError(f"Invalid start_date format: {e}")
        
        if end_date:
            try:
                end_dt = pd.to_datetime(end_date)
                df = df[df.index <= end_dt]
                logger.info(f"Filtered data until {end_date}")
            except Exception as e:
                raise DataLoadingError(f"Invalid end_date format: {e}")
        
        if df.empty:
            raise DataLoadingError("No data remaining after date filtering")
        
        # Resample if needed
        if frequency == "W":
            df = df.resample("W").last()
            logger.info("Resampled to weekly frequency")
        elif frequency == "M":
            df = df.resample("M").last()
            logger.info("Resampled to monthly frequency")
        
        logger.info(f"Successfully loaded {len(df)} observations")
        return df
        
    except pd.errors.EmptyDataError:
        raise DataLoadingError(f"File is empty: {file_path}")
    except pd.errors.ParserError as e:
        raise DataLoadingError(f"Failed to parse CSV file: {e}")
    except Exception as e:
        if isinstance(e, DataLoadingError):
            raise
        raise DataLoadingError(f"Unexpected error loading data: {e}")


def validate_data(df: pd.DataFrame) -> Dict:
    """
    Validate data quality and return validation report with error handling.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame with time series data
    
    Returns:
    --------
    dict
        Validation report with statistics
    
    Raises:
    -------
    DataValidationError
        If DataFrame is invalid or empty
    """
    if df is None:
        raise DataValidationError("DataFrame is None")
    
    if not isinstance(df, pd.DataFrame):
        raise DataValidationError(f"Expected DataFrame, got {type(df)}")
    
    if df.empty:
        raise DataValidationError("DataFrame is empty")
    
    try:
        report = {
            "total_observations": len(df),
            "date_range": (df.index.min(), df.index.max()),
            "missing_values": df.isnull().sum().to_dict(),
            "missing_percentage": (df.isnull().sum() / len(df) * 100).to_dict(),
            "duplicate_dates": df.index.duplicated().sum(),
            "data_types": df.dtypes.to_dict(),
        }
        
        # Check for outliers (using IQR method)
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) == 0:
            logger.warning("No numeric columns found in DataFrame")
            report["outliers"] = {}
        else:
            outliers = {}
            for col in numeric_cols:
                try:
                    Q1 = df[col].quantile(0.25)
                    Q3 = df[col].quantile(0.75)
                    IQR = Q3 - Q1
                    
                    if IQR == 0:
                        logger.warning(f"IQR is zero for column {col}, skipping outlier detection")
                        outliers[col] = {"count": 0, "percentage": 0.0}
                    else:
                        lower_bound = Q1 - 1.5 * IQR
                        upper_bound = Q3 + 1.5 * IQR
                        outliers[col] = {
                            "count": int(((df[col] < lower_bound) | (df[col] > upper_bound)).sum()),
                            "percentage": float(((df[col] < lower_bound) | (df[col] > upper_bound)).sum() / len(df) * 100)
                        }
                except Exception as e:
                    logger.warning(f"Failed to calculate outliers for {col}: {e}")
                    outliers[col] = {"count": 0, "percentage": 0.0}
            
            report["outliers"] = outliers
        
        logger.info(f"Validation completed: {len(df)} observations, {len(numeric_cols)} numeric columns")
        return report
        
    except Exception as e:
        raise DataValidationError(f"Error during validation: {e}")


def preprocess_data(df: pd.DataFrame, handle_missing: str = "forward_fill") -> pd.DataFrame:
    """
    Preprocess time series data with error handling.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame
    handle_missing : str
        Method to handle missing values: 'forward_fill', 'backward_fill', 'interpolate', 'drop'
    
    Returns:
    --------
    pd.DataFrame
        Preprocessed DataFrame
    
    Raises:
    -------
    ValueError
        If handle_missing method is invalid
    DataValidationError
        If preprocessing fails
    """
    if df is None or df.empty:
        raise DataValidationError("Cannot preprocess empty or None DataFrame")
    
    valid_methods = ["forward_fill", "backward_fill", "interpolate", "drop"]
    if handle_missing not in valid_methods:
        raise ValueError(f"Invalid handle_missing method: {handle_missing}. Must be one of {valid_methods}")
    
    try:
        df_processed = df.copy()
        
        if handle_missing == "forward_fill":
            df_processed = df_processed.ffill()
        elif handle_missing == "backward_fill":
            df_processed = df_processed.bfill()
        elif handle_missing == "interpolate":
            df_processed = df_processed.interpolate(method="time")
        elif handle_missing == "drop":
            df_processed = df_processed.dropna()
        
        if df_processed.empty:
            raise DataValidationError("DataFrame is empty after preprocessing")
        
        logger.info(f"Preprocessed data: {len(df_processed)} observations remaining")
        return df_processed
        
    except Exception as e:
        raise DataValidationError(f"Error during preprocessing: {e}")


def load_event_data(file_path: str = "data/raw/oil_market_events.csv") -> pd.DataFrame:
    """
    Load event data from CSV file with error handling.
    
    Parameters:
    -----------
    file_path : str
        Path to event data CSV file
    
    Returns:
    --------
    pd.DataFrame
        DataFrame with event information
    
    Raises:
    -------
    DataLoadingError
        If file cannot be loaded or is invalid
    """
    file_path_obj = Path(file_path)
    
    if not file_path_obj.exists():
        raise DataLoadingError(f"Event data file not found: {file_path}")
    
    try:
        logger.info(f"Loading event data from {file_path}")
        df = pd.read_csv(file_path, parse_dates=["event_date"])
        
        if df.empty:
            raise DataLoadingError("Event data file is empty")
        
        # Validate required columns
        required_columns = ["event_date"]
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            raise DataLoadingError(f"Missing required columns: {missing_columns}")
        
        logger.info(f"Successfully loaded {len(df)} events")
        return df
        
    except pd.errors.EmptyDataError:
        raise DataLoadingError(f"Event data file is empty: {file_path}")
    except pd.errors.ParserError as e:
        raise DataLoadingError(f"Failed to parse event data CSV: {e}")
    except Exception as e:
        if isinstance(e, DataLoadingError):
            raise
        raise DataLoadingError(f"Unexpected error loading event data: {e}")
