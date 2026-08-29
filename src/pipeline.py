"""
End-to-End ETL and Analytics Pipeline Orchestrator.
"""

import sys
import json
import logging
from pathlib import Path
import pandas as pd
from sqlalchemy import text

from src.config import RAW_DATA_DIR, PROCESSED_DATA_DIR, SQL_DIR, SQLITE_DB_PATH
from src.data_loader import load_all_raw_datasets, validate_raw_datasets
from src.data_cleaning import clean_all_datasets
from src.feature_engineering import build_analytics_star_schema
from src.database import get_database_engine, load_dataframe_to_table, execute_sql_file, run_query

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s - %(message)s"
)
logger = logging.getLogger("Pipeline")


def run_pipeline(save_csv: bool = True, load_db: bool = True) -> dict:
    """
    Execute complete end-to-end data pipeline:
    1. Load Raw Datasets
    2. Clean and Standardize (Staging)
    3. Feature Engineering & Star Schema Construction (Analytics)
    4. Persist Processed Data Files
    5. Ingest into SQL Database
    6. Run Quality Checks & Compute Core Business Metrics
    """
    logger.info("=" * 60)
    logger.info("STARTING SALES & BI ANALYTICS PIPELINE")
    logger.info("=" * 60)
    
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    # 1. Load Raw Data
    logger.info("[Step 1/6] Loading Raw Datasets...")
    raw_data = load_all_raw_datasets(RAW_DATA_DIR)
    if not validate_raw_datasets(raw_data):
        raise ValueError("Raw data validation failed.")
        
    # 2. Clean & Stage Data
    logger.info("[Step 2/6] Cleaning and Standardizing Staging Tables...")
    staging_data = clean_all_datasets(raw_data)
    
    # 3. Feature Engineering & Star Schema Modeling
    logger.info("[Step 3/6] Engineering Features & Dimensional Modeling...")
    analytics_model = build_analytics_star_schema(staging_data)
    
    # 4. Save Processed Files
    if save_csv:
        logger.info("[Step 4/6] Saving Processed Data to data/processed/...")
        for name, df in analytics_model.items():
            out_csv = PROCESSED_DATA_DIR / f"{name}.csv"
            df.to_csv(out_csv, index=False)
            logger.info(f"Saved {out_csv.name} ({len(df):,} rows)")
            
    # 5. Load into Database
    engine, db_type = get_database_engine()
    if load_db:
        logger.info(f"[Step 5/6] Ingesting Data into {db_type.upper()} Database...")
        
        # Load raw layer
        for name, df in raw_data.items():
            schema_name = "raw" if db_type == "postgres" else None
            tbl_name = f"raw_{name}" if db_type == "sqlite" else name
            load_dataframe_to_table(df, tbl_name, engine, schema=schema_name)
            
        # Load staging layer
        for name, df in staging_data.items():
            schema_name = "staging" if db_type == "postgres" else None
            tbl_name = f"stg_{name}" if db_type == "sqlite" else name
            load_dataframe_to_table(df, tbl_name, engine, schema=schema_name)
            
        # Load analytics star schema
        for name, df in analytics_model.items():
            schema_name = "analytics" if db_type == "postgres" else None
            tbl_name = f"analytics_{name}" if db_type == "sqlite" else name
            load_dataframe_to_table(df, tbl_name, engine, schema=schema_name)
            
    # 6. Compute Key Business Metrics Summary
    logger.info("[Step 6/6] Computing Core Business KPIs & Metrics...")
    fact_sales = analytics_model['fact_sales']
    fact_orders = analytics_model['fact_orders']
    dim_customer = analytics_model['dim_customer']
    fact_reviews = analytics_model['fact_reviews']
    
    delivered_orders = fact_orders[fact_orders['order_status'] == 'delivered']
    
    total_revenue = float(fact_sales['item_value'].sum())
    total_product_revenue = float(fact_sales['price'].sum())
    total_freight_value = float(fact_sales['freight_value'].sum())
    total_orders_count = int(fact_orders['order_id'].nunique())
    delivered_orders_count = int(delivered_orders['order_id'].nunique())
    total_customers_count = int(dim_customer['customer_unique_id'].nunique())
    
    aov = float(total_revenue / total_orders_count) if total_orders_count > 0 else 0.0
    items_per_order = float(len(fact_sales) / total_orders_count) if total_orders_count > 0 else 0.0
    
    repeat_customers = int(dim_customer['is_repeat_customer'].sum())
    repeat_rate = float(repeat_customers / len(dim_customer)) * 100 if len(dim_customer) > 0 else 0.0
    
    avg_delivery_days = float(delivered_orders['delivery_days'].mean())
    late_orders_count = int(delivered_orders['is_late'].sum())
    late_delivery_rate = float(late_orders_count / delivered_orders_count) * 100 if delivered_orders_count > 0 else 0.0
    
    avg_review_score = float(fact_reviews['review_score'].mean())
    
    metrics = {
        "total_revenue": round(total_revenue, 2),
        "total_product_revenue": round(total_product_revenue, 2),
        "total_freight_value": round(total_freight_value, 2),
        "total_orders": total_orders_count,
        "delivered_orders": delivered_orders_count,
        "total_customers": total_customers_count,
        "average_order_value": round(aov, 2),
        "items_per_order": round(items_per_order, 2),
        "repeat_customers_count": repeat_customers,
        "repeat_customer_rate_pct": round(repeat_rate, 2),
        "average_delivery_days": round(avg_delivery_days, 1),
        "late_delivery_count": late_orders_count,
        "late_delivery_rate_pct": round(late_delivery_rate, 2),
        "average_review_score": round(avg_review_score, 2)
    }
    
    metrics_path = PROCESSED_DATA_DIR / "business_metrics.json"
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=4)
        
    logger.info("=" * 60)
    logger.info(f"PIPELINE COMPLETED SUCCESSFULLY!")
    logger.info(f"Total Revenue: R$ {metrics['total_revenue']:,.2f}")
    logger.info(f"Total Orders: {metrics['total_orders']:,}")
    logger.info(f"Total Customers: {metrics['total_customers']:,}")
    logger.info(f"Average Order Value: R$ {metrics['average_order_value']:,.2f}")
    logger.info(f"Avg Delivery Days: {metrics['average_delivery_days']} days (Late Rate: {metrics['late_delivery_rate_pct']}%)")
    logger.info(f"Avg Review Score: {metrics['average_review_score']} / 5.0")
    logger.info("=" * 60)
    
    return {
        "metrics": metrics,
        "analytics_model": analytics_model,
        "staging_data": staging_data
    }


if __name__ == "__main__":
    run_pipeline()
