"""
Backend utility functions for validation, error handling, and data transformation.

This module provides reusable utilities following DRY principles:
- Input validation
- Error response formatting
- Date parsing and validation
- Data transformation helpers
"""

from flask import jsonify
from datetime import datetime
import pandas as pd
import logging
from typing import Optional, Tuple, Dict, Any

logger = logging.getLogger(__name__)


class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass


class APIError(Exception):
    """Custom exception for API errors."""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


def validate_date_string(date_string: str, parameter_name: str = "date") -> pd.Timestamp:
    """
    Validate and parse a date string.
    
    Args:
        date_string: Date string in YYYY-MM-DD format
        parameter_name: Name of the parameter for error messages
        
    Returns:
        pd.Timestamp: Parsed datetime object
        
    Raises:
        ValidationError: If date string is invalid
    """
    if not date_string or not isinstance(date_string, str):
        raise ValidationError(f"{parameter_name} must be a non-empty string")
    
    try:
        parsed_date = pd.to_datetime(date_string, format='%Y-%m-%d')
        if pd.isna(parsed_date):
            raise ValidationError(f"{parameter_name} could not be parsed as a valid date")
        return parsed_date
    except (ValueError, TypeError) as e:
        raise ValidationError(f"Invalid {parameter_name} format '{date_string}'. Expected YYYY-MM-DD format: {str(e)}")


def validate_date_range(start_date: Optional[str], end_date: Optional[str]) -> Tuple[Optional[pd.Timestamp], Optional[pd.Timestamp]]:
    """
    Validate a date range ensuring start_date <= end_date.
    
    Args:
        start_date: Start date string (YYYY-MM-DD) or None
        end_date: End date string (YYYY-MM-DD) or None
        
    Returns:
        Tuple of (start_timestamp, end_timestamp) or (None, None)
        
    Raises:
        ValidationError: If dates are invalid or start_date > end_date
    """
    start_dt = None
    end_dt = None
    
    if start_date:
        start_dt = validate_date_string(start_date, "start_date")
    
    if end_date:
        end_dt = validate_date_string(end_date, "end_date")
    
    if start_dt and end_dt and start_dt > end_dt:
        raise ValidationError(
            f"start_date ({start_date}) must be less than or equal to end_date ({end_date})"
        )
    
    return start_dt, end_dt


def validate_filter_value(filter_value: str, allowed_values: list, filter_name: str) -> str:
    """
    Validate that a filter value is in the allowed list.
    
    Args:
        filter_value: The filter value to validate
        allowed_values: List of allowed values
        filter_name: Name of the filter for error messages
        
    Returns:
        str: The validated filter value
        
    Raises:
        ValidationError: If filter value is not in allowed list
    """
    if not filter_value:
        return filter_value
    
    if filter_value not in allowed_values:
        raise ValidationError(
            f"Invalid {filter_name} '{filter_value}'. Allowed values: {', '.join(allowed_values)}"
        )
    
    return filter_value


def create_error_response(error_message: str, status_code: int = 400, error_type: str = "ValidationError") -> Tuple[Dict[str, Any], int]:
    """
    Create a standardized error response.
    
    Args:
        error_message: Human-readable error message
        status_code: HTTP status code
        error_type: Type of error (ValidationError, APIError, etc.)
        
    Returns:
        Tuple of (error_dict, status_code) for Flask jsonify
    """
    error_response = {
        "error": error_message,
        "error_type": error_type,
        "status_code": status_code
    }
    
    logger.warning(f"API Error ({status_code}): {error_message}")
    return error_response, status_code


def create_success_response(data: Any, status_code: int = 200, message: Optional[str] = None) -> Dict[str, Any]:
    """
    Create a standardized success response.
    
    Args:
        data: Response data
        status_code: HTTP status code
        message: Optional success message
        
    Returns:
        Dict with success response structure
    """
    response = {
        "data": data,
        "status": "success",
        "status_code": status_code
    }
    
    if message:
        response["message"] = message
    
    return response


def apply_date_filter_to_dataframe(
    dataframe: pd.DataFrame,
    date_column: str,
    start_date: Optional[pd.Timestamp],
    end_date: Optional[pd.Timestamp]
) -> pd.DataFrame:
    """
    Apply date range filter to a DataFrame.
    
    Args:
        dataframe: DataFrame to filter
        date_column: Name of the date column (or 'index' for index-based)
        start_date: Start date timestamp or None
        end_date: End date timestamp or None
        
    Returns:
        Filtered DataFrame
        
    Raises:
        ValidationError: If date column doesn't exist or filtering fails
    """
    filtered_df = dataframe.copy()
    
    if date_column == 'index':
        date_series = filtered_df.index
    else:
        if date_column not in filtered_df.columns:
            raise ValidationError(f"Date column '{date_column}' not found in dataframe")
        date_series = filtered_df[date_column]
    
    if start_date:
        if date_column == 'index':
            filtered_df = filtered_df[date_series >= start_date]
        else:
            filtered_df = filtered_df[date_series >= start_date]
    
    if end_date:
        if date_column == 'index':
            filtered_df = filtered_df[date_series <= end_date]
        else:
            filtered_df = filtered_df[date_series <= end_date]
    
    return filtered_df


def convert_dataframe_to_json_serializable(dataframe: pd.DataFrame, date_columns: list = None) -> list:
    """
    Convert DataFrame to JSON-serializable list of dictionaries.
    
    Args:
        dataframe: DataFrame to convert
        date_columns: List of column names that contain dates
        
    Returns:
        List of dictionaries with dates converted to strings
    """
    if date_columns is None:
        date_columns = []
    
    records = dataframe.to_dict('records')
    
    for record in records:
        for col in date_columns:
            if col in record and pd.notna(record[col]):
                if isinstance(record[col], pd.Timestamp):
                    record[col] = record[col].strftime('%Y-%m-%d')
                elif hasattr(record[col], 'strftime'):
                    record[col] = record[col].strftime('%Y-%m-%d')
    
    return records


def validate_dataframe_not_empty(dataframe: pd.DataFrame, dataframe_name: str = "DataFrame") -> None:
    """
    Validate that a DataFrame is not empty.
    
    Args:
        dataframe: DataFrame to validate
        dataframe_name: Name for error messages
        
    Raises:
        ValidationError: If DataFrame is empty
    """
    if dataframe is None:
        raise ValidationError(f"{dataframe_name} is None")
    
    if len(dataframe) == 0:
        raise ValidationError(f"{dataframe_name} is empty")


def get_query_parameter(request, param_name: str, default: Optional[str] = None, required: bool = False) -> Optional[str]:
    """
    Safely get and validate a query parameter.
    
    Args:
        request: Flask request object
        param_name: Name of the query parameter
        default: Default value if parameter is not provided
        required: Whether the parameter is required
        
    Returns:
        Parameter value or default
        
    Raises:
        ValidationError: If required parameter is missing
    """
    value = request.args.get(param_name, default)
    
    if required and (value is None or value == ''):
        raise ValidationError(f"Required query parameter '{param_name}' is missing")
    
    return value
