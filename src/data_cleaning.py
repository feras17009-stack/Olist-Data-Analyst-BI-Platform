"""
Data cleaning and standardization module for Olist E-Commerce dataset.
"""

import re
import logging
from typing import Dict, Tuple
import pandas as pd
import numpy as np

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def to_snake_case(text: str) -> str:
    """Standardize column names to snake_case."""
    s = re.sub(r'[\s\-]+', '_', text.strip())
    s = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s)
    return s.lower()


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Rename all columns in a dataframe to snake_case."""
    df = df.copy()
    df.columns = [to_snake_case(c) for c in df.columns]
    return df


def clean_customers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean and standardize customers dataset.
    """
    logger.info("Cleaning customers dataset...")
    df = clean_column_names(df)
    
    df['customer_id'] = df['customer_id'].astype(str).str.strip()
    df['customer_unique_id'] = df['customer_unique_id'].astype(str).str.strip()
    df['customer_zip_code_prefix'] = pd.to_numeric(df['customer_zip_code_prefix'], errors='coerce').fillna(0).astype(int)
    df['customer_city'] = df['customer_city'].astype(str).str.strip().str.title()
    df['customer_state'] = df['customer_state'].astype(str).str.strip().str.upper()
    
    # Drop pure duplicate customer IDs if any
    df = df.drop_duplicates(subset=['customer_id'])
    logger.info(f"Cleaned customers shape: {df.shape}")
    return df


def clean_orders(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean orders dataset, convert timestamps and handle missing timestamps logically.
    """
    logger.info("Cleaning orders dataset...")
    df = clean_column_names(df)
    
    df['order_id'] = df['order_id'].astype(str).str.strip()
    df['customer_id'] = df['customer_id'].astype(str).str.strip()
    df['order_status'] = df['order_status'].astype(str).str.strip().str.lower()
    
    # Datetime fields
    datetime_cols = [
        'order_purchase_timestamp',
        'order_approved_at',
        'order_delivered_carrier_date',
        'order_delivered_customer_date',
        'order_estimated_delivery_date'
    ]
    
    for col in datetime_cols:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
            
    df = df.drop_duplicates(subset=['order_id'])
    logger.info(f"Cleaned orders shape: {df.shape}")
    return df


def clean_order_items(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean order items dataset, ensure numeric prices and positive freight values.
    """
    logger.info("Cleaning order items dataset...")
    df = clean_column_names(df)
    
    df['order_id'] = df['order_id'].astype(str).str.strip()
    df['order_item_id'] = pd.to_numeric(df['order_item_id'], errors='coerce').fillna(1).astype(int)
    df['product_id'] = df['product_id'].astype(str).str.strip()
    df['seller_id'] = df['seller_id'].astype(str).str.strip()
    
    if 'shipping_limit_date' in df.columns:
        df['shipping_limit_date'] = pd.to_datetime(df['shipping_limit_date'], errors='coerce')
        
    df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0.0)
    df['freight_value'] = pd.to_numeric(df['freight_value'], errors='coerce').fillna(0.0)
    
    # Financial data validation: prices and freight must be non-negative
    df = df[(df['price'] >= 0) & (df['freight_value'] >= 0)]
    df = df.drop_duplicates(subset=['order_id', 'order_item_id'])
    
    logger.info(f"Cleaned order items shape: {df.shape}")
    return df


def clean_order_payments(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean payments dataset and standardize payment types.
    """
    logger.info("Cleaning payments dataset...")
    df = clean_column_names(df)
    
    df['order_id'] = df['order_id'].astype(str).str.strip()
    df['payment_sequential'] = pd.to_numeric(df['payment_sequential'], errors='coerce').fillna(1).astype(int)
    df['payment_type'] = df['payment_type'].astype(str).str.strip().str.lower()
    df['payment_installments'] = pd.to_numeric(df['payment_installments'], errors='coerce').fillna(1).astype(int)
    df['payment_value'] = pd.to_numeric(df['payment_value'], errors='coerce').fillna(0.0)
    
    # Filter non-negative payments
    df = df[df['payment_value'] >= 0]
    
    # Normalize undefined payment types
    df['payment_type'] = df['payment_type'].replace({'not_defined': 'other'})
    
    logger.info(f"Cleaned payments shape: {df.shape}")
    return df


def clean_order_reviews(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean reviews dataset, cast scores and parse timestamps.
    """
    logger.info("Cleaning reviews dataset...")
    df = clean_column_names(df)
    
    df['review_id'] = df['review_id'].astype(str).str.strip()
    df['order_id'] = df['order_id'].astype(str).str.strip()
    df['review_score'] = pd.to_numeric(df['review_score'], errors='coerce').fillna(0).astype(int)
    
    # Validate review score range (1 to 5)
    df = df[(df['review_score'] >= 1) & (df['review_score'] <= 5)]
    
    if 'review_creation_date' in df.columns:
        df['review_creation_date'] = pd.to_datetime(df['review_creation_date'], errors='coerce')
    if 'review_answer_timestamp' in df.columns:
        df['review_answer_timestamp'] = pd.to_datetime(df['review_answer_timestamp'], errors='coerce')
        
    df['review_comment_title'] = df['review_comment_title'].fillna('').astype(str).str.strip()
    df['review_comment_message'] = df['review_comment_message'].fillna('').astype(str).str.strip()
    
    # De-duplicate: Keep the latest review record per order
    if 'review_answer_timestamp' in df.columns:
        df = df.sort_values(by='review_answer_timestamp', ascending=False)
    df = df.drop_duplicates(subset=['order_id', 'review_id'])
    
    logger.info(f"Cleaned reviews shape: {df.shape}")
    return df


def clean_products(df: pd.DataFrame, translation_df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean products dataset and join English category translations.
    """
    logger.info("Cleaning products dataset...")
    df = clean_column_names(df)
    trans = clean_column_names(translation_df)
    
    df['product_id'] = df['product_id'].astype(str).str.strip()
    
    # Rename typo in original dataset: 'lenght' -> 'length'
    df = df.rename(columns={
        'product_name_lenght': 'product_name_length',
        'product_description_lenght': 'product_description_length'
    })
    
    # Merge translation
    df = df.merge(
        trans[['product_category_name', 'product_category_name_english']], 
        on='product_category_name', 
        how='left'
    )
    
    # Fill missing category names
    df['product_category_name'] = df['product_category_name'].fillna('desconhecido')
    df['product_category_name_english'] = df['product_category_name_english'].fillna('unknown')
    
    # Clean numeric physical dimensions
    numeric_cols = [
        'product_name_length', 'product_description_length', 'product_photos_qty',
        'product_weight_g', 'product_length_cm', 'product_height_cm', 'product_width_cm'
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
            
    df = df.drop_duplicates(subset=['product_id'])
    logger.info(f"Cleaned products shape: {df.shape}")
    return df


def clean_sellers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean sellers dataset.
    """
    logger.info("Cleaning sellers dataset...")
    df = clean_column_names(df)
    
    df['seller_id'] = df['seller_id'].astype(str).str.strip()
    df['seller_zip_code_prefix'] = pd.to_numeric(df['seller_zip_code_prefix'], errors='coerce').fillna(0).astype(int)
    df['seller_city'] = df['seller_city'].astype(str).str.strip().str.title()
    df['seller_state'] = df['seller_state'].astype(str).str.strip().str.upper()
    
    df = df.drop_duplicates(subset=['seller_id'])
    logger.info(f"Cleaned sellers shape: {df.shape}")
    return df


def clean_geolocation(df: pd.DataFrame) -> pd.DataFrame:
    """
    Clean geolocation dataset and aggregate by zip code prefix to remove redundant coordinates.
    """
    logger.info("Cleaning and aggregating geolocation dataset...")
    df = clean_column_names(df)
    
    df['geolocation_zip_code_prefix'] = pd.to_numeric(df['geolocation_zip_code_prefix'], errors='coerce').fillna(0).astype(int)
    df['geolocation_lat'] = pd.to_numeric(df['geolocation_lat'], errors='coerce')
    df['geolocation_lng'] = pd.to_numeric(df['geolocation_lng'], errors='coerce')
    df['geolocation_city'] = df['geolocation_city'].astype(str).str.strip().str.title()
    df['geolocation_state'] = df['geolocation_state'].astype(str).str.strip().str.upper()
    
    # Filter plausible GPS coordinates for Brazil (Lat ~ +5 to -35, Lng ~ -75 to -30)
    valid_coords = (
        (df['geolocation_lat'] >= -35) & (df['geolocation_lat'] <= 6) &
        (df['geolocation_lng'] >= -75) & (df['geolocation_lng'] <= -30)
    )
    df = df[valid_coords]
    
    # Aggregate median latitude/longitude and modal city/state per zip prefix
    geo_agg = df.groupby('geolocation_zip_code_prefix').agg(
        latitude=('geolocation_lat', 'median'),
        longitude=('geolocation_lng', 'median'),
        city=('geolocation_city', lambda x: x.mode()[0] if not x.empty else ''),
        state=('geolocation_state', lambda x: x.mode()[0] if not x.empty else '')
    ).reset_index()
    
    logger.info(f"Aggregated geolocation shape: {geo_agg.shape}")
    return geo_agg


def clean_all_datasets(raw_dict: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    """
    Execute end-to-end data cleaning across all datasets.
    """
    cleaned = {}
    cleaned['stg_customers'] = clean_customers(raw_dict['customers'])
    cleaned['stg_orders'] = clean_orders(raw_dict['orders'])
    cleaned['stg_order_items'] = clean_order_items(raw_dict['order_items'])
    cleaned['stg_order_payments'] = clean_order_payments(raw_dict['order_payments'])
    cleaned['stg_order_reviews'] = clean_order_reviews(raw_dict['order_reviews'])
    cleaned['stg_products'] = clean_products(raw_dict['products'], raw_dict['category_translation'])
    cleaned['stg_sellers'] = clean_sellers(raw_dict['sellers'])
    cleaned['stg_geolocation'] = clean_geolocation(raw_dict['geolocation'])
    
    logger.info("All staging datasets cleaned successfully.")
    return cleaned
