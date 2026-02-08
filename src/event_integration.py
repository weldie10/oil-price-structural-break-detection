"""
Event data integration and analysis module.

This module provides functions for integrating event data with price data
and analyzing event impacts with comprehensive error handling.
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from datetime import timedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EventIntegrationError(Exception):
    """Custom exception for event integration errors."""
    pass


def align_events_with_prices(
    price_df: pd.DataFrame,
    event_df: pd.DataFrame,
    price_column: str = "price",
    event_date_column: str = "event_date",
    window_days: int = 30
) -> pd.DataFrame:
    """
    Align event dates with price data and calculate price movements with error handling.
    
    Parameters:
    -----------
    price_df : pd.DataFrame
        DataFrame with price data (date index)
    event_df : pd.DataFrame
        DataFrame with event data
    price_column : str
        Name of price column in price_df
    event_date_column : str
        Name of event date column in event_df
    window_days : int
        Number of days before/after event to analyze (must be positive)
    
    Returns:
    --------
    pd.DataFrame
        Event data with price impact metrics
    
    Raises:
    -------
    EventIntegrationError
        If integration fails or inputs are invalid
    """
    # Input validation
    if price_df is None or price_df.empty:
        raise EventIntegrationError("Price DataFrame is None or empty")
    
    if event_df is None or event_df.empty:
        raise EventIntegrationError("Event DataFrame is None or empty")
    
    if price_column not in price_df.columns:
        raise EventIntegrationError(f"Price column '{price_column}' not found in price_df")
    
    if event_date_column not in event_df.columns:
        raise EventIntegrationError(f"Event date column '{event_date_column}' not found in event_df")
    
    if window_days <= 0:
        raise ValueError(f"window_days must be positive, got {window_days}")
    
    if not isinstance(price_df.index, pd.DatetimeIndex):
        raise EventIntegrationError("Price DataFrame must have DatetimeIndex")
    
    try:
        event_analysis = event_df.copy()
        
        # Ensure event dates are datetime
        try:
            event_analysis[event_date_column] = pd.to_datetime(event_analysis[event_date_column])
        except Exception as e:
            raise EventIntegrationError(f"Failed to convert event dates to datetime: {e}")
        
        # Initialize columns for price metrics
        event_analysis["price_before"] = np.nan
        event_analysis["price_after"] = np.nan
        event_analysis["price_change"] = np.nan
        event_analysis["price_change_pct"] = np.nan
        event_analysis["max_price_window"] = np.nan
        event_analysis["min_price_window"] = np.nan
        event_analysis["volatility_window"] = np.nan
        
        successful_alignments = 0
        
        for idx, row in event_analysis.iterrows():
            try:
                event_date = row[event_date_column]
                
                if pd.isna(event_date):
                    logger.warning(f"Skipping row {idx}: event_date is NaN")
                    continue
                
                # Define window
                window_start = event_date - timedelta(days=window_days)
                window_end = event_date + timedelta(days=window_days)
                
                # Get prices in window
                window_prices = price_df[
                    (price_df.index >= window_start) & (price_df.index <= window_end)
                ][price_column]
                
                if len(window_prices) == 0:
                    logger.warning(f"No price data found for event at {event_date}")
                    continue
                
                # Price before event (average of days before)
                before_prices = price_df[
                    (price_df.index >= window_start) & (price_df.index < event_date)
                ][price_column]
                
                # Price after event (average of days after)
                after_prices = price_df[
                    (price_df.index > event_date) & (price_df.index <= window_end)
                ][price_column]
                
                if len(before_prices) > 0 and len(after_prices) > 0:
                    price_before = before_prices.mean()
                    price_after = after_prices.mean()
                    
                    event_analysis.at[idx, "price_before"] = price_before
                    event_analysis.at[idx, "price_after"] = price_after
                    event_analysis.at[idx, "price_change"] = price_after - price_before
                    
                    if price_before != 0:
                        event_analysis.at[idx, "price_change_pct"] = (
                            (price_after - price_before) / price_before * 100
                        )
                    
                    event_analysis.at[idx, "max_price_window"] = window_prices.max()
                    event_analysis.at[idx, "min_price_window"] = window_prices.min()
                    event_analysis.at[idx, "volatility_window"] = window_prices.std()
                    
                    successful_alignments += 1
                else:
                    logger.warning(f"Insufficient price data before/after event at {event_date}")
                    
            except Exception as e:
                logger.error(f"Error processing event at row {idx}: {e}")
                continue
        
        logger.info(f"Successfully aligned {successful_alignments} out of {len(event_analysis)} events")
        return event_analysis
        
    except Exception as e:
        if isinstance(e, (EventIntegrationError, ValueError)):
            raise
        raise EventIntegrationError(f"Unexpected error in event alignment: {e}")


def categorize_events(event_df: pd.DataFrame) -> Dict[str, pd.DataFrame]:
    """
    Categorize events by type.
    
    Parameters:
    -----------
    event_df : pd.DataFrame
        Event DataFrame
    
    Returns:
    --------
    dict
        Dictionary with event categories as keys
    """
    categories = {}
    
    if "event_type" in event_df.columns:
        for event_type in event_df["event_type"].unique():
            categories[event_type] = event_df[event_df["event_type"] == event_type]
    
    if "impact_type" in event_df.columns:
        for impact_type in event_df["impact_type"].unique():
            key = f"impact_{impact_type}"
            categories[key] = event_df[event_df["impact_type"] == impact_type]
    
    return categories


def calculate_event_impact_statistics(event_df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate summary statistics for event impacts.
    
    Parameters:
    -----------
    event_df : pd.DataFrame
        Event DataFrame with price impact metrics
    
    Returns:
    --------
    pd.DataFrame
        Summary statistics by event category
    """
    stats_list = []
    
    # Overall statistics
    if "price_change_pct" in event_df.columns:
        overall_stats = {
            "category": "Overall",
            "count": len(event_df),
            "mean_price_change_pct": event_df["price_change_pct"].mean(),
            "median_price_change_pct": event_df["price_change_pct"].median(),
            "std_price_change_pct": event_df["price_change_pct"].std(),
            "max_price_change_pct": event_df["price_change_pct"].max(),
            "min_price_change_pct": event_df["price_change_pct"].min(),
        }
        stats_list.append(overall_stats)
        
        # By event type
        if "event_type" in event_df.columns:
            for event_type in event_df["event_type"].unique():
                type_df = event_df[event_df["event_type"] == event_type]
                type_stats = {
                    "category": f"Type: {event_type}",
                    "count": len(type_df),
                    "mean_price_change_pct": type_df["price_change_pct"].mean(),
                    "median_price_change_pct": type_df["price_change_pct"].median(),
                    "std_price_change_pct": type_df["price_change_pct"].std(),
                    "max_price_change_pct": type_df["price_change_pct"].max(),
                    "min_price_change_pct": type_df["price_change_pct"].min(),
                }
                stats_list.append(type_stats)
        
        # By impact type
        if "impact_type" in event_df.columns:
            for impact_type in event_df["impact_type"].unique():
                impact_df = event_df[event_df["impact_type"] == impact_type]
                impact_stats = {
                    "category": f"Impact: {impact_type}",
                    "count": len(impact_df),
                    "mean_price_change_pct": impact_df["price_change_pct"].mean(),
                    "median_price_change_pct": impact_df["price_change_pct"].median(),
                    "std_price_change_pct": impact_df["price_change_pct"].std(),
                    "max_price_change_pct": impact_df["price_change_pct"].max(),
                    "min_price_change_pct": impact_df["price_change_pct"].min(),
                }
                stats_list.append(impact_stats)
    
    return pd.DataFrame(stats_list)
