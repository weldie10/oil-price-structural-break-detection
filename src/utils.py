"""
Utility functions for common operations across the project.

This module provides reusable functions for date parsing, data validation,
error handling, and other common operations to ensure consistency and
reduce code duplication.
"""

import pandas as pd
import numpy as np
from typing import Optional, Union, List, Tuple
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def parse_date_string(date_string: Optional[str], parameter_name: str = "date") -> Optional[pd.Timestamp]:
    """
    Parse a date string into a pandas Timestamp with consistent error handling.
    
    Parameters:
    -----------
    date_string : str or None
        Date string in 'YYYY-MM-DD' format
    parameter_name : str
        Name of the parameter for error messages
    
    Returns:
    --------
    pd.Timestamp or None
        Parsed timestamp, or None if input is None
    
    Raises:
    -------
    ValueError
        If date string cannot be parsed
    """
    if date_string is None:
        return None
    
    if not isinstance(date_string, str):
        raise ValueError(f"{parameter_name} must be a string, got {type(date_string)}")
    
    try:
        parsed_date = pd.to_datetime(date_string)
        return parsed_date
    except (ValueError, TypeError) as e:
        raise ValueError(f"Invalid {parameter_name} format '{date_string}'. Expected 'YYYY-MM-DD' format. Error: {e}")


def ensure_datetime_index(df: pd.DataFrame, index_name: str = "index") -> pd.DataFrame:
    """
    Ensure DataFrame has a DatetimeIndex, converting if necessary.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Input DataFrame
    index_name : str
        Name for error messages
    
    Returns:
    --------
    pd.DataFrame
        DataFrame with DatetimeIndex
    
    Raises:
    -------
    ValueError
        If index cannot be converted to datetime
    """
    if df is None:
        raise ValueError(f"{index_name} DataFrame is None")
    
    if not isinstance(df.index, pd.DatetimeIndex):
        try:
            df = df.copy()
            df.index = pd.to_datetime(df.index)
            logger.debug(f"Converted {index_name} to DatetimeIndex")
        except (ValueError, TypeError) as e:
            raise ValueError(f"Failed to convert {index_name} to DatetimeIndex: {e}")
    
    return df


def validate_dataframe_not_empty(df: pd.DataFrame, dataframe_name: str = "DataFrame") -> None:
    """
    Validate that a DataFrame is not None or empty.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame to validate
    dataframe_name : str
        Name for error messages
    
    Raises:
    -------
    ValueError
        If DataFrame is None or empty
    """
    if df is None:
        raise ValueError(f"{dataframe_name} is None")
    
    if not isinstance(df, pd.DataFrame):
        raise ValueError(f"{dataframe_name} must be a pandas DataFrame, got {type(df)}")
    
    if df.empty:
        raise ValueError(f"{dataframe_name} is empty")


def validate_required_columns(df: pd.DataFrame, required_columns: List[str], dataframe_name: str = "DataFrame") -> None:
    """
    Validate that DataFrame contains all required columns.
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame to validate
    required_columns : list of str
        List of required column names
    dataframe_name : str
        Name for error messages
    
    Raises:
    -------
    ValueError
        If any required columns are missing
    """
    validate_dataframe_not_empty(df, dataframe_name)
    
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(
            f"{dataframe_name} is missing required columns: {missing_columns}. "
            f"Available columns: {list(df.columns)}"
        )


def validate_positive_integer(value: int, parameter_name: str = "value") -> None:
    """
    Validate that a value is a positive integer.
    
    Parameters:
    -----------
    value : int
        Value to validate
    parameter_name : str
        Name for error messages
    
    Raises:
    -------
    ValueError
        If value is not a positive integer
    """
    if not isinstance(value, int):
        raise ValueError(f"{parameter_name} must be an integer, got {type(value)}")
    
    if value <= 0:
        raise ValueError(f"{parameter_name} must be positive, got {value}")


def validate_file_path(file_path: Union[str, Path], must_exist: bool = True) -> Path:
    """
    Validate and normalize a file path.
    
    Parameters:
    -----------
    file_path : str or Path
        File path to validate
    must_exist : bool
        Whether the file must exist
    
    Returns:
    --------
    Path
        Normalized Path object
    
    Raises:
    -------
    ValueError
        If path is invalid or file doesn't exist when required
    """
    if file_path is None:
        raise ValueError("File path cannot be None")
    
    try:
        path_obj = Path(file_path)
    except (TypeError, ValueError) as e:
        raise ValueError(f"Invalid file path '{file_path}': {e}")
    
    if must_exist and not path_obj.exists():
        raise FileNotFoundError(f"File not found: {path_obj}")
    
    return path_obj


def calculate_price_statistics_in_window(
    price_series: pd.Series,
    start_date: pd.Timestamp,
    end_date: pd.Timestamp
) -> dict:
    """
    Calculate price statistics within a date window with error handling.
    
    Parameters:
    -----------
    price_series : pd.Series
        Price time series with DatetimeIndex
    start_date : pd.Timestamp
        Start of window
    end_date : pd.Timestamp
        End of window
    
    Returns:
    --------
    dict
        Dictionary with price statistics (mean, min, max, std, count)
    
    Raises:
    -------
    ValueError
        If dates are invalid or no data in window
    """
    if not isinstance(price_series.index, pd.DatetimeIndex):
        raise ValueError("price_series must have DatetimeIndex")
    
    if start_date >= end_date:
        raise ValueError(f"start_date ({start_date}) must be before end_date ({end_date})")
    
    window_data = price_series[(price_series.index >= start_date) & (price_series.index <= end_date)]
    
    if window_data.empty:
        return {
            "mean": np.nan,
            "min": np.nan,
            "max": np.nan,
            "std": np.nan,
            "count": 0
        }
    
    return {
        "mean": float(window_data.mean()),
        "min": float(window_data.min()),
        "max": float(window_data.max()),
        "std": float(window_data.std()),
        "count": len(window_data)
    }


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    Safely divide two numbers, returning default if denominator is zero.
    
    Parameters:
    -----------
    numerator : float
        Numerator
    denominator : float
        Denominator
    default : float
        Default value if denominator is zero
    
    Returns:
    --------
    float
        Result of division or default value
    """
    if denominator == 0 or np.isnan(denominator):
        return default
    return numerator / denominator


def format_percentage(value: float, decimals: int = 2) -> str:
    """
    Format a float as a percentage string.
    
    Parameters:
    -----------
    value : float
        Value to format (e.g., 0.15 for 15%)
    decimals : int
        Number of decimal places
    
    Returns:
    --------
    str
        Formatted percentage string
    """
    return f"{value * 100:.{decimals}f}%"


def create_error_response(message: str, status_code: int = 400, error_type: str = "ValidationError") -> dict:
    """
    Create a standardized error response dictionary.
    
    Parameters:
    -----------
    message : str
        Error message
    status_code : int
        HTTP status code (for API responses)
    error_type : str
        Type of error
    
    Returns:
    --------
    dict
        Standardized error response
    """
    return {
        "error": {
            "type": error_type,
            "message": message,
            "status_code": status_code
        },
        "success": False
    }


def create_success_response(data: dict, message: Optional[str] = None) -> dict:
    """
    Create a standardized success response dictionary.
    
    Parameters:
    -----------
    data : dict
        Response data
    message : str, optional
        Success message
    
    Returns:
    --------
    dict
        Standardized success response
    """
    response = {
        "data": data,
        "success": True
    }
    
    if message:
        response["message"] = message
    
    return response
