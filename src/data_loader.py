"""
Data loader module for reading and validating raw Olist dataset files.
"""

import logging
from pathlib import Path
from typing import Dict, Optional
import pandas as pd

from src.config import RAW_DATA_DIR, RAW_FILES

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def load_raw_dataset(dataset_name: str, raw_dir: Optional[Path] = None) -> pd.DataFrame:
    """
    Load a single raw dataset by key name.
    
    Args:
        dataset_name: Key corresponding to RAW_FILES dictionary.
        raw_dir: Path to directory containing raw CSVs.
        
    Returns:
        pd.DataFrame containing the raw data.
    """
    if dataset_name not in RAW_FILES:
        raise ValueError(f"Unknown dataset: {dataset_name}. Valid keys: {list(RAW_FILES.keys())}")
    
    directory = raw_dir or RAW_DATA_DIR
    file_path = directory / RAW_FILES[dataset_name]
    
    if not file_path.exists():
        raise FileNotFoundError(f"Raw data file not found at {file_path}")
    
    logger.info(f"Loading {dataset_name} from {file_path.name}...")
    df = pd.read_csv(file_path)
    logger.info(f"Loaded {dataset_name}: {df.shape[0]:,} rows, {df.shape[1]} columns.")
    return df


def load_all_raw_datasets(raw_dir: Optional[Path] = None) -> Dict[str, pd.DataFrame]:
    """
    Load all 9 raw datasets into a dictionary.
    
    Args:
        raw_dir: Path to raw directory.
        
    Returns:
        Dict[str, pd.DataFrame]: Dictionary of dataset name to DataFrame.
    """
    directory = raw_dir or RAW_DATA_DIR
    logger.info(f"Loading all raw datasets from {directory}...")
    
    datasets = {}
    for key in RAW_FILES:
        datasets[key] = load_raw_dataset(key, directory)
        
    logger.info(f"Successfully loaded all {len(datasets)} datasets.")
    return datasets


def validate_raw_datasets(datasets: Dict[str, pd.DataFrame]) -> bool:
    """
    Validate that loaded raw datasets have expected minimum row counts and key columns.
    
    Returns:
        bool: True if validation passes.
    """
    expected_columns = {
        "customers": ["customer_id", "customer_unique_id", "customer_zip_code_prefix", "customer_city", "customer_state"],
        "orders": ["order_id", "customer_id", "order_status", "order_purchase_timestamp"],
        "order_items": ["order_id", "order_item_id", "product_id", "seller_id", "price", "freight_value"],
        "order_payments": ["order_id", "payment_sequential", "payment_type", "payment_value"],
        "order_reviews": ["review_id", "order_id", "review_score"],
        "products": ["product_id"],
        "sellers": ["seller_id"],
        "geolocation": ["geolocation_zip_code_prefix", "geolocation_lat", "geolocation_lng"],
        "category_translation": ["product_category_name", "product_category_name_english"]
    }
    
    for key, cols in expected_columns.items():
        if key not in datasets:
            logger.error(f"Missing dataset: {key}")
            return False
        df = datasets[key]
        for col in cols:
            if col not in df.columns:
                logger.error(f"Missing column '{col}' in dataset '{key}'")
                return False
        if len(df) == 0:
            logger.error(f"Dataset '{key}' is empty!")
            return False
            
    logger.info("Raw dataset schema and integrity validation PASSED.")
    return True


if __name__ == "__main__":
    data = load_all_raw_datasets()
    assert validate_raw_datasets(data), "Validation failed"
    print("All datasets loaded and verified successfully.")
