"""
Exploratory Data Analysis module for time series properties.

This module provides functions for analyzing time series properties including
trend, stationarity, and volatility with comprehensive error handling.
"""

import pandas as pd
import numpy as np
from scipy import stats
from statsmodels.tsa.stattools import adfuller, kpss, acf, pacf
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.stats.diagnostic import acorr_ljungbox
from typing import Dict, Tuple, Optional
import warnings
import logging

from .utils import (
    validate_dataframe_not_empty,
    validate_positive_integer,
    safe_divide
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class EDAError(Exception):
    """Custom exception for EDA analysis errors."""
    pass


def descriptive_statistics(df: pd.DataFrame, periods: list = None) -> pd.DataFrame:
    """
    Calculate descriptive statistics across different time periods.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Time series data
    periods : list, optional
        List of period labels and date ranges
    
    Returns:
    --------
    pd.DataFrame
        Statistics for each period
    """
    stats_dict = {}
    
    if periods:
        for period_name, (start, end) in periods:
            period_data = df[(df.index >= start) & (df.index <= end)]
            stats_dict[period_name] = calculate_stats(period_data)
    else:
        stats_dict["full_period"] = calculate_stats(df)
    
    return pd.DataFrame(stats_dict).T


def calculate_stats(df: pd.DataFrame) -> Dict:
    """Calculate statistics for a DataFrame."""
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    stats_dict = {}
    
    for col in numeric_cols:
        stats_dict[f"{col}_mean"] = df[col].mean()
        stats_dict[f"{col}_std"] = df[col].std()
        stats_dict[f"{col}_var"] = df[col].var()
        stats_dict[f"{col}_skew"] = df[col].skew()
        stats_dict[f"{col}_kurtosis"] = df[col].kurtosis()
        stats_dict[f"{col}_min"] = df[col].min()
        stats_dict[f"{col}_max"] = df[col].max()
    
    return stats_dict


def trend_analysis(df: pd.DataFrame, window: int = 30) -> Dict:
    """
    Perform trend analysis on time series with error handling.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Time series data
    window : int
        Window size for moving average (must be positive)
    
    Returns:
    --------
    dict
        Trend analysis results
    
    Raises:
    -------
    EDAError
        If analysis fails or inputs are invalid
    """
    # Validate DataFrame using utility function
    try:
        validate_dataframe_not_empty(df, dataframe_name="Input DataFrame")
    except ValueError as e:
        raise EDAError(str(e))
    
    # Validate window parameter using utility function
    try:
        validate_positive_integer(window, parameter_name="window")
    except ValueError as e:
        raise EDAError(str(e))
        raise ValueError(f"Window must be positive, got {window}")
    
    if window > len(df):
        raise ValueError(f"Window ({window}) exceeds data length ({len(df)})")
    
    try:
        results = {}
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        
        if len(numeric_cols) == 0:
            raise EDAError("No numeric columns found in DataFrame")
        
        for col in numeric_cols:
            try:
                # Moving averages
                if len(df[col].dropna()) < window:
                    logger.warning(f"Insufficient data for {col}: {len(df[col].dropna())} < {window}")
                    continue
                
                results[f"{col}_ma_{window}"] = df[col].rolling(window=window).mean()
                results[f"{col}_ma_{window*2}"] = df[col].rolling(window=window*2).mean()
                
                # Linear trend
                col_data = df[col].dropna()
                if len(col_data) < 2:
                    logger.warning(f"Insufficient data for linear trend in {col}")
                    continue
                
                x = np.arange(len(col_data))
                slope, intercept, r_value, p_value, std_err = stats.linregress(x, col_data.values)
                results[f"{col}_linear_trend"] = {
                    "slope": float(slope),
                    "intercept": float(intercept),
                    "r_squared": float(r_value**2),
                    "p_value": float(p_value)
                }
                
                # Time series decomposition
                try:
                    min_period = 2 * window if len(col_data) > 2 * window else None
                    if min_period is None or len(col_data) < min_period:
                        logger.warning(f"Insufficient data for decomposition in {col}")
                    else:
                        decomposition = seasonal_decompose(
                            col_data,
                            model="additive",
                            period=min(365, len(col_data) // 2) if len(col_data) > 730 else None
                        )
                        results[f"{col}_trend"] = decomposition.trend
                        results[f"{col}_seasonal"] = decomposition.seasonal
                        results[f"{col}_residual"] = decomposition.resid
                except Exception as e:
                    logger.warning(f"Decomposition failed for {col}: {e}")
                    
            except Exception as e:
                logger.error(f"Error processing column {col}: {e}")
                continue
        
        if not results:
            raise EDAError("No trend analysis results generated")
        
        logger.info(f"Trend analysis completed for {len(numeric_cols)} columns")
        return results
        
    except Exception as e:
        if isinstance(e, (EDAError, ValueError)):
            raise
        raise EDAError(f"Unexpected error in trend analysis: {e}")


def test_stationarity(series: pd.Series, alpha: float = 0.05) -> Dict:
    """
    Test for stationarity using multiple tests with error handling.
    
    Parameters:
    -----------
    series : pd.Series
        Time series to test
    alpha : float
        Significance level (must be between 0 and 1)
    
    Returns:
    --------
    dict
        Test results
    
    Raises:
    -------
    EDAError
        If testing fails or inputs are invalid
    """
    if series is None:
        raise EDAError("Series is None")
    
    if not isinstance(series, pd.Series):
        raise EDAError(f"Expected Series, got {type(series)}")
    
    if not (0 < alpha < 1):
        raise ValueError(f"Alpha must be between 0 and 1, got {alpha}")
    
    # Remove NaN values
    series_clean = series.dropna()
    
    if len(series_clean) < 10:
        raise EDAError(f"Insufficient data for stationarity testing: {len(series_clean)} observations (minimum 10 required)")
    
    results = {}
    
    # Augmented Dickey-Fuller test
    try:
        adf_result = adfuller(series_clean, autolag="AIC")
        results["adf"] = {
            "test_statistic": float(adf_result[0]),
            "p_value": float(adf_result[1]),
            "critical_values": {k: float(v) for k, v in adf_result[4].items()},
            "is_stationary": adf_result[1] < alpha
        }
    except Exception as e:
        logger.warning(f"ADF test failed: {e}")
        results["adf"] = None
    
    # KPSS test
    try:
        kpss_result = kpss(series_clean, regression="ct", nlags="auto")
        results["kpss"] = {
            "test_statistic": float(kpss_result[0]),
            "p_value": float(kpss_result[1]),
            "critical_values": {k: float(v) for k, v in kpss_result[3].items()},
            "is_stationary": kpss_result[1] > alpha
        }
    except Exception as e:
        logger.warning(f"KPSS test failed: {e}")
        results["kpss"] = None
    
    # Combined interpretation
    if results["adf"] and results["kpss"]:
        adf_stationary = results["adf"]["is_stationary"]
        kpss_stationary = results["kpss"]["is_stationary"]
        
        if adf_stationary and kpss_stationary:
            results["conclusion"] = "Stationary"
        elif not adf_stationary and not kpss_stationary:
            results["conclusion"] = "Non-stationary"
        else:
            results["conclusion"] = "Inconclusive - conflicting results"
    else:
        results["conclusion"] = "Unable to determine"
    
    logger.info(f"Stationarity test completed: {results.get('conclusion', 'Unknown')}")
    return results


def volatility_analysis(df: pd.DataFrame, window: int = 30) -> Dict:
    """
    Analyze volatility patterns in time series.
    
    Parameters:
    -----------
    df : pd.DataFrame
        Time series data
    window : int
        Window size for rolling volatility
    
    Returns:
    --------
    dict
        Volatility analysis results
    """
    results = {}
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    
    for col in numeric_cols:
        # Returns
        returns = df[col].pct_change().dropna()
        log_returns = np.log(df[col] / df[col].shift(1)).dropna()
        
        # Rolling volatility
        results[f"{col}_rolling_volatility"] = returns.rolling(window=window).std()
        results[f"{col}_rolling_volatility_annualized"] = (
            returns.rolling(window=window).std() * np.sqrt(252)
        )
        
        # Volatility statistics
        results[f"{col}_volatility_stats"] = {
            "mean_volatility": returns.std(),
            "annualized_volatility": returns.std() * np.sqrt(252),
            "max_volatility": results[f"{col}_rolling_volatility"].max(),
            "min_volatility": results[f"{col}_rolling_volatility"].min(),
            "volatility_of_volatility": results[f"{col}_rolling_volatility"].std()
        }
        
        # Test for ARCH effects (volatility clustering)
        try:
            # Ljung-Box test on squared returns
            lb_test = acorr_ljungbox(returns**2, lags=10, return_df=True)
            results[f"{col}_arch_test"] = {
                "ljung_box_statistic": lb_test["lb_stat"].iloc[-1],
                "p_value": lb_test["lb_pvalue"].iloc[-1],
                "has_arch_effects": lb_test["lb_pvalue"].iloc[-1] < 0.05
            }
        except Exception as e:
            warnings.warn(f"ARCH test failed for {col}: {e}")
            results[f"{col}_arch_test"] = None
    
    return results


def autocorrelation_analysis(series: pd.Series, lags: int = 40) -> Tuple[np.ndarray, np.ndarray]:
    """
    Calculate autocorrelation and partial autocorrelation functions.
    
    Parameters:
    -----------
    series : pd.Series
        Time series data
    lags : int
        Number of lags to compute
    
    Returns:
    --------
    tuple
        (ACF values, PACF values)
    """
    series_clean = series.dropna()
    
    acf_values = acf(series_clean, nlags=lags, fft=True)
    pacf_values = pacf(series_clean, nlags=lags)
    
    return acf_values, pacf_values
