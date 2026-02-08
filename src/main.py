"""
Main module demonstrating modular design and usage of the oil price analysis package.

This module showcases:
- Modular design with separate concerns (data loading, EDA, event integration)
- Error handling throughout the pipeline
- Clear structure and organization
- Usage examples for all modules
"""

import sys
from pathlib import Path
import logging

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Import modules
from data_loader import (
    load_oil_price_data,
    validate_data,
    preprocess_data,
    load_event_data,
    DataLoadingError,
    DataValidationError
)
from eda import (
    descriptive_statistics,
    trend_analysis,
    test_stationarity,
    volatility_analysis,
    EDAError
)
from event_integration import (
    align_events_with_prices,
    categorize_events,
    calculate_event_impact_statistics,
    EventIntegrationError
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_analysis_pipeline(
    price_file_path: str = None,
    event_file_path: str = "data/raw/oil_market_events.csv",
    start_date: str = None,
    end_date: str = None
) -> dict:
    """
    Run the complete analysis pipeline demonstrating modular design.
    
    This function demonstrates:
    1. Data loading with error handling
    2. Data validation
    3. Data preprocessing
    4. Exploratory data analysis
    5. Event integration
    6. Error handling at each step
    
    Parameters:
    -----------
    price_file_path : str, optional
        Path to price data CSV file
    event_file_path : str
        Path to event data CSV file
    start_date : str, optional
        Start date for filtering data
    end_date : str, optional
        End date for filtering data
    
    Returns:
    --------
    dict
        Dictionary containing all analysis results
    
    Raises:
    -------
    Various custom exceptions from modules
    """
    results = {}
    
    try:
        # Step 1: Load price data
        logger.info("="*80)
        logger.info("STEP 1: Loading Price Data")
        logger.info("="*80)
        
        if price_file_path is None:
            logger.warning("No price file path provided. Skipping price data loading.")
            logger.info("To load price data, provide a CSV file with Brent crude prices.")
            return {"error": "No price data file provided"}
        
        try:
            price_df = load_oil_price_data(
                file_path=price_file_path,
                start_date=start_date,
                end_date=end_date,
                frequency="D"
            )
            results["price_data"] = price_df
            logger.info(f"✓ Successfully loaded {len(price_df)} price observations")
        except DataLoadingError as e:
            logger.error(f"Failed to load price data: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error loading price data: {e}")
            raise DataLoadingError(f"Unexpected error: {e}")
        
        # Step 2: Validate price data
        logger.info("\n" + "="*80)
        logger.info("STEP 2: Validating Price Data")
        logger.info("="*80)
        
        try:
            validation_report = validate_data(price_df)
            results["validation_report"] = validation_report
            logger.info("✓ Data validation completed")
            logger.info(f"  Total observations: {validation_report['total_observations']}")
            logger.info(f"  Date range: {validation_report['date_range']}")
        except DataValidationError as e:
            logger.error(f"Data validation failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in validation: {e}")
            raise
        
        # Step 3: Preprocess data
        logger.info("\n" + "="*80)
        logger.info("STEP 3: Preprocessing Data")
        logger.info("="*80)
        
        try:
            price_df_clean = preprocess_data(price_df, handle_missing="forward_fill")
            results["price_data_clean"] = price_df_clean
            logger.info(f"✓ Data preprocessing completed: {len(price_df_clean)} observations")
        except DataValidationError as e:
            logger.error(f"Data preprocessing failed: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in preprocessing: {e}")
            raise
        
        # Step 4: Exploratory Data Analysis
        logger.info("\n" + "="*80)
        logger.info("STEP 4: Exploratory Data Analysis")
        logger.info("="*80)
        
        # 4.1 Descriptive Statistics
        try:
            desc_stats = descriptive_statistics(price_df_clean)
            results["descriptive_statistics"] = desc_stats
            logger.info("✓ Descriptive statistics calculated")
        except Exception as e:
            logger.warning(f"Descriptive statistics failed: {e}")
        
        # 4.2 Trend Analysis
        try:
            trend_results = trend_analysis(price_df_clean, window=30)
            results["trend_analysis"] = trend_results
            logger.info("✓ Trend analysis completed")
        except EDAError as e:
            logger.error(f"Trend analysis failed: {e}")
        except Exception as e:
            logger.error(f"Unexpected error in trend analysis: {e}")
        
        # 4.3 Stationarity Testing
        try:
            price_col = price_df_clean.columns[0]
            stationarity_results = test_stationarity(price_df_clean[price_col])
            results["stationarity_test"] = stationarity_results
            logger.info(f"✓ Stationarity testing completed: {stationarity_results.get('conclusion', 'Unknown')}")
        except EDAError as e:
            logger.error(f"Stationarity testing failed: {e}")
        except Exception as e:
            logger.error(f"Unexpected error in stationarity testing: {e}")
        
        # 4.4 Volatility Analysis
        try:
            volatility_results = volatility_analysis(price_df_clean, window=30)
            results["volatility_analysis"] = volatility_results
            logger.info("✓ Volatility analysis completed")
        except Exception as e:
            logger.error(f"Volatility analysis failed: {e}")
        
        # Step 5: Load and integrate event data
        logger.info("\n" + "="*80)
        logger.info("STEP 5: Event Data Integration")
        logger.info("="*80)
        
        try:
            events_df = load_event_data(event_file_path)
            results["event_data"] = events_df
            logger.info(f"✓ Loaded {len(events_df)} events")
        except DataLoadingError as e:
            logger.error(f"Failed to load event data: {e}")
            # Continue without event data
            events_df = None
        
        if events_df is not None and price_df_clean is not None:
            try:
                events_with_prices = align_events_with_prices(
                    price_df=price_df_clean,
                    event_df=events_df,
                    price_column=price_df_clean.columns[0],
                    window_days=30
                )
                results["events_with_prices"] = events_with_prices
                logger.info("✓ Event-price alignment completed")
                
                # Calculate impact statistics
                impact_stats = calculate_event_impact_statistics(events_with_prices)
                results["event_impact_stats"] = impact_stats
                logger.info("✓ Event impact statistics calculated")
                
            except EventIntegrationError as e:
                logger.error(f"Event integration failed: {e}")
            except Exception as e:
                logger.error(f"Unexpected error in event integration: {e}")
        
        logger.info("\n" + "="*80)
        logger.info("ANALYSIS PIPELINE COMPLETED SUCCESSFULLY")
        logger.info("="*80)
        
        return results
        
    except (DataLoadingError, DataValidationError, EDAError, EventIntegrationError) as e:
        logger.error(f"\nPipeline failed with custom error: {e}")
        results["error"] = str(e)
        return results
    except Exception as e:
        logger.error(f"\nPipeline failed with unexpected error: {e}")
        results["error"] = f"Unexpected error: {e}"
        return results


def main():
    """
    Main entry point demonstrating modular design usage.
    """
    logger.info("Oil Price Analysis - Modular Design Demonstration")
    logger.info("="*80)
    
    # Example usage - replace with actual file paths
    price_file = "data/raw/brent_prices.csv"  # User should provide this
    event_file = "data/raw/oil_market_events.csv"
    
    # Check if price file exists
    if not Path(price_file).exists():
        logger.warning(f"Price file not found: {price_file}")
        logger.info("To run the full pipeline, provide a CSV file with Brent crude prices.")
        logger.info("The pipeline will demonstrate error handling for missing data.")
    
    # Run the analysis pipeline
    results = run_analysis_pipeline(
        price_file_path=price_file if Path(price_file).exists() else None,
        event_file_path=event_file,
        start_date="2000-01-01",
        end_date="2024-12-31"
    )
    
    # Display summary
    if "error" in results:
        logger.error(f"Pipeline completed with errors: {results['error']}")
    else:
        logger.info("\nPipeline Results Summary:")
        logger.info(f"  - Price data loaded: {'price_data' in results}")
        logger.info(f"  - Data validated: {'validation_report' in results}")
        logger.info(f"  - EDA completed: {'trend_analysis' in results}")
        logger.info(f"  - Events integrated: {'events_with_prices' in results}")


if __name__ == "__main__":
    main()
