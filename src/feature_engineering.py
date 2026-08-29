"""
Feature Engineering and Dimensional Modeling module for Olist Analytics Platform.
"""

import logging
from typing import Dict, Tuple
import pandas as pd
import numpy as np

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def create_date_dimension(start_date: str = "2016-01-01", end_date: str = "2018-12-31") -> pd.DataFrame:
    """
    Generate a comprehensive calendar dimension table (dim_date).
    """
    logger.info(f"Generating dim_date from {start_date} to {end_date}...")
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    dim_date = pd.DataFrame({'full_date': dates})
    dim_date['date_key'] = dim_date['full_date'].dt.strftime('%Y%m%d').astype(int)
    dim_date['year'] = dim_date['full_date'].dt.year
    dim_date['quarter'] = dim_date['full_date'].dt.quarter
    dim_date['quarter_name'] = 'Q' + dim_date['quarter'].astype(str) + ' ' + dim_date['year'].astype(str)
    dim_date['month'] = dim_date['full_date'].dt.month
    dim_date['month_name'] = dim_date['full_date'].dt.strftime('%B')
    dim_date['year_month'] = dim_date['full_date'].dt.strftime('%Y-%m')
    dim_date['week'] = dim_date['full_date'].dt.isocalendar().week.astype(int)
    dim_date['day'] = dim_date['full_date'].dt.day
    dim_date['day_of_week'] = dim_date['full_date'].dt.dayofweek + 1  # 1=Monday, 7=Sunday
    dim_date['day_name'] = dim_date['full_date'].dt.strftime('%A')
    dim_date['is_weekend'] = dim_date['day_of_week'].isin([6, 7]).astype(int)
    dim_date['is_month_end'] = dim_date['full_date'].dt.is_month_end.astype(int)
    
    logger.info(f"Generated dim_date with {len(dim_date)} days.")
    return dim_date


def engineer_delivery_features(orders_df: pd.DataFrame) -> pd.DataFrame:
    """
    Add delivery duration, delay, and lateness metrics.
    """
    df = orders_df.copy()
    
    # Delivery duration in days (delivered - purchased)
    df['delivery_days'] = (
        df['order_delivered_customer_date'] - df['order_purchase_timestamp']
    ).dt.total_seconds() / 86400.0
    
    # Estimated delivery duration in days
    df['estimated_delivery_days'] = (
        df['order_estimated_delivery_date'] - df['order_purchase_timestamp']
    ).dt.total_seconds() / 86400.0
    
    # Delay days relative to estimated delivery date (positive = late, negative = early)
    df['delay_days'] = (
        df['order_delivered_customer_date'] - df['order_estimated_delivery_date']
    ).dt.total_seconds() / 86400.0
    
    # Delivery status flags
    df['is_delivered'] = (
        (df['order_status'] == 'delivered') & df['order_delivered_customer_date'].notna()
    ).astype(int)
    
    # is_late flag: 1 if delivered after estimated date, 0 otherwise
    df['is_late'] = (
        (df['is_delivered'] == 1) & 
        (df['order_delivered_customer_date'] > df['order_estimated_delivery_date'])
    ).astype(int)
    
    # Date key for date dimension join
    df['purchase_date_key'] = df['order_purchase_timestamp'].dt.strftime('%Y%m%d').fillna('19000101').astype(int)
    
    return df


def calculate_rfm_segments(
    customers_df: pd.DataFrame, 
    orders_df: pd.DataFrame, 
    items_df: pd.DataFrame
) -> pd.DataFrame:
    """
    Compute RFM (Recency, Frequency, Monetary) metrics and assign customer segments.
    """
    logger.info("Calculating RFM customer segmentation...")
    
    # Merge valid orders with customer unique ID and order items
    valid_orders = orders_df[orders_df['order_status'] != 'canceled'].copy()
    
    # Order items totals per order
    order_rev = items_df.groupby('order_id').agg(
        order_revenue=('price', 'sum'),
        order_freight=('freight_value', 'sum')
    ).reset_index()
    order_rev['total_order_value'] = order_rev['order_revenue'] + order_rev['order_freight']
    
    merged = valid_orders.merge(customers_df[['customer_id', 'customer_unique_id']], on='customer_id', how='inner')
    merged = merged.merge(order_rev, on='order_id', how='left')
    merged['total_order_value'] = merged['total_order_value'].fillna(0.0)
    
    # Reference snapshot date: 1 day after max purchase date in dataset
    snapshot_date = orders_df['order_purchase_timestamp'].max() + pd.Timedelta(days=1)
    
    # Customer level aggregation
    rfm = merged.groupby('customer_unique_id').agg(
        recency_days=('order_purchase_timestamp', lambda x: (snapshot_date - x.max()).days),
        frequency=('order_id', 'nunique'),
        monetary=('total_order_value', 'sum'),
        first_purchase_date=('order_purchase_timestamp', 'min'),
        last_purchase_date=('order_purchase_timestamp', 'max')
    ).reset_index()
    
    # Quantile binning for RFM scoring (1-4)
    # Recency: lower days = better score (4 is best, 1 is worst)
    # Frequency: most customers have 1 order, so use custom bins [1, 2, 3+]
    # Monetary: higher value = better score (4 is best, 1 is worst)
    
    r_labels = [4, 3, 2, 1]
    m_labels = [1, 2, 3, 4]
    
    rfm['r_score'] = pd.qcut(rfm['recency_days'], q=4, labels=r_labels, duplicates='drop').astype(int)
    
    def get_f_score(freq: int) -> int:
        if freq == 1:
            return 1
        elif freq == 2:
            return 3
        else:
            return 4
            
    rfm['f_score'] = rfm['frequency'].apply(get_f_score)
    rfm['m_score'] = pd.qcut(rfm['monetary'].rank(method='first'), q=4, labels=m_labels).astype(int)
    
    rfm['rfm_score'] = (
        rfm['r_score'].astype(str) + 
        rfm['f_score'].astype(str) + 
        rfm['m_score'].astype(str)
    )
    
    # Segment Assignment Rules
    def segment_customer(row) -> str:
        r = row['r_score']
        f = row['f_score']
        m = row['m_score']
        
        if r >= 4 and f >= 3:
            return 'Champions'
        elif r >= 3 and f >= 3:
            return 'Loyal Customers'
        elif r >= 3 and f >= 1 and m >= 3:
            return 'Potential Loyalists'
        elif r >= 4 and f == 1:
            return 'New Customers'
        elif r == 3 and f == 1:
            return 'Promising Recent'
        elif r == 2 and f >= 2:
            return 'Customers Needing Attention'
        elif r == 2 and f == 1:
            return 'About To Sleep'
        elif r == 1 and f >= 2:
            return 'At Risk'
        else:
            return 'Lost / Hibernating'
            
    rfm['rfm_segment'] = rfm.apply(segment_customer, axis=1)
    rfm['is_repeat_customer'] = (rfm['frequency'] > 1).astype(int)
    
    logger.info(f"RFM Segmentation completed for {len(rfm)} unique customers.")
    return rfm


def build_analytics_star_schema(staging: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    """
    Transform staging data into a production star schema (analytics dimensional model).
    """
    logger.info("Building analytics star schema dimensional model...")
    
    stg_customers = staging['stg_customers']
    stg_orders = engineer_delivery_features(staging['stg_orders'])
    stg_items = staging['stg_order_items']
    stg_payments = staging['stg_order_payments']
    stg_reviews = staging['stg_order_reviews']
    stg_products = staging['stg_products']
    stg_sellers = staging['stg_sellers']
    stg_geo = staging['stg_geolocation']
    
    # 1. Date Dimension
    dim_date = create_date_dimension("2016-01-01", "2018-12-31")
    
    # 2. RFM & Customer Dimension
    rfm = calculate_rfm_segments(stg_customers, stg_orders, stg_items)
    
    # dim_customer (grain: customer_id with unique_id and rfm attributes)
    dim_customer = stg_customers.merge(rfm, on='customer_unique_id', how='left')
    dim_customer['customer_key'] = np.arange(1, len(dim_customer) + 1)
    dim_customer['rfm_recency'] = dim_customer['recency_days'].fillna(0).astype(int)
    dim_customer['rfm_frequency'] = dim_customer['frequency'].fillna(1).astype(int)
    dim_customer['rfm_monetary'] = dim_customer['monetary'].fillna(0.0).round(2)
    dim_customer['rfm_segment'] = dim_customer['rfm_segment'].fillna('New Customers')
    dim_customer['is_repeat_customer'] = dim_customer['is_repeat_customer'].fillna(0).astype(int)
    
    # 3. Product Dimension
    dim_product = stg_products.copy()
    dim_product['product_key'] = np.arange(1, len(dim_product) + 1)
    
    # 4. Seller Dimension
    dim_seller = stg_sellers.copy()
    dim_seller['seller_key'] = np.arange(1, len(dim_seller) + 1)
    
    # 5. Location Dimension
    dim_location = stg_geo.copy()
    dim_location['location_key'] = np.arange(1, len(dim_location) + 1)
    
    # 6. Fact Orders (Grain: one row per order)
    # Order items summary
    items_summary = stg_items.groupby('order_id').agg(
        order_item_count=('order_item_id', 'count'),
        total_order_value=('price', 'sum'),
        total_freight_value=('freight_value', 'sum')
    ).reset_index()
    
    # Merge keys to fact_orders
    fact_orders = stg_orders.merge(
        dim_customer[['customer_id', 'customer_key', 'customer_state']], 
        on='customer_id', 
        how='left'
    )
    fact_orders = fact_orders.merge(items_summary, on='order_id', how='left')
    fact_orders['order_item_count'] = fact_orders['order_item_count'].fillna(0).astype(int)
    fact_orders['total_order_value'] = fact_orders['total_order_value'].fillna(0.0).round(2)
    fact_orders['total_freight_value'] = fact_orders['total_freight_value'].fillna(0.0).round(2)
    fact_orders['total_order_amount'] = (fact_orders['total_order_value'] + fact_orders['total_freight_value']).round(2)
    fact_orders['order_key'] = np.arange(1, len(fact_orders) + 1)
    
    # 7. Fact Sales (Grain: one row per order item)
    fact_sales = stg_items.merge(
        stg_orders[['order_id', 'customer_id', 'order_status', 'purchase_date_key']], 
        on='order_id', 
        how='inner'
    )
    fact_sales = fact_sales.merge(
        dim_customer[['customer_id', 'customer_key']], 
        on='customer_id', 
        how='left'
    )
    fact_sales = fact_sales.merge(
        dim_product[['product_id', 'product_key']], 
        on='product_id', 
        how='left'
    )
    fact_sales = fact_sales.merge(
        dim_seller[['seller_id', 'seller_key']], 
        on='seller_id', 
        how='left'
    )
    fact_sales['item_value'] = (fact_sales['price'] + fact_sales['freight_value']).round(2)
    fact_sales['sales_key'] = np.arange(1, len(fact_sales) + 1)
    fact_sales['date_key'] = fact_sales['purchase_date_key']
    
    # 8. Fact Payments (Grain: one payment transaction)
    fact_payments = stg_payments.copy()
    fact_payments = fact_payments.merge(
        stg_orders[['order_id', 'purchase_date_key']], 
        on='order_id', 
        how='left'
    )
    fact_payments['date_key'] = fact_payments['purchase_date_key'].fillna(19000101).astype(int)
    fact_payments['payment_key'] = np.arange(1, len(fact_payments) + 1)
    
    # 9. Fact Reviews (Grain: one review record)
    fact_reviews = stg_reviews.copy()
    fact_reviews['has_comment'] = (
        (fact_reviews['review_comment_title'] != '') | 
        (fact_reviews['review_comment_message'] != '')
    ).astype(int)
    fact_reviews = fact_reviews.merge(
        stg_orders[['order_id', 'purchase_date_key']], 
        on='order_id', 
        how='left'
    )
    fact_reviews['date_key'] = fact_reviews['purchase_date_key'].fillna(19000101).astype(int)
    fact_reviews['review_record_key'] = np.arange(1, len(fact_reviews) + 1)
    
    analytics_model = {
        "dim_date": dim_date,
        "dim_customer": dim_customer,
        "dim_product": dim_product,
        "dim_seller": dim_seller,
        "dim_location": dim_location,
        "fact_orders": fact_orders,
        "fact_sales": fact_sales,
        "fact_payments": fact_payments,
        "fact_reviews": fact_reviews
    }
    
    logger.info("Star schema dimensional model constructed successfully.")
    return analytics_model
