"""
Integration tests for data quality and integrity on the generated star schema datasets.
"""

import pytest
import pandas as pd
from pathlib import Path
from src.config import PROCESSED_DATA_DIR


@pytest.fixture(scope="module")
def datasets():
    files = {
        "dim_date": PROCESSED_DATA_DIR / "dim_date.csv",
        "dim_customer": PROCESSED_DATA_DIR / "dim_customer.csv",
        "dim_product": PROCESSED_DATA_DIR / "dim_product.csv",
        "dim_seller": PROCESSED_DATA_DIR / "dim_seller.csv",
        "dim_location": PROCESSED_DATA_DIR / "dim_location.csv",
        "fact_orders": PROCESSED_DATA_DIR / "fact_orders.csv",
        "fact_sales": PROCESSED_DATA_DIR / "fact_sales.csv",
        "fact_payments": PROCESSED_DATA_DIR / "fact_payments.csv",
        "fact_reviews": PROCESSED_DATA_DIR / "fact_reviews.csv"
    }
    
    loaded = {}
    for k, p in files.items():
        assert p.exists(), f"Processed file missing: {p}"
        loaded[k] = pd.read_csv(p)
    return loaded


def test_primary_key_uniqueness(datasets):
    """Verify primary keys are 100% unique and non-null."""
    assert datasets["dim_date"]["date_key"].is_unique
    assert datasets["dim_customer"]["customer_key"].is_unique
    assert datasets["dim_product"]["product_key"].is_unique
    assert datasets["dim_seller"]["seller_key"].is_unique
    assert datasets["dim_location"]["location_key"].is_unique
    assert datasets["fact_orders"]["order_id"].is_unique
    assert datasets["fact_sales"]["sales_key"].is_unique
    assert datasets["fact_payments"]["payment_key"].is_unique
    assert datasets["fact_reviews"]["review_record_key"].is_unique


def test_referential_integrity(datasets):
    """Verify that all foreign keys in fact tables match corresponding dimension primary keys."""
    sales = datasets["fact_sales"]
    customers = datasets["dim_customer"]
    products = datasets["dim_product"]
    sellers = datasets["dim_seller"]
    
    # Customer FK in fact_sales
    orphan_customers = set(sales["customer_key"].dropna()) - set(customers["customer_key"])
    assert len(orphan_customers) == 0, f"Found orphan customer keys: {orphan_customers}"
    
    # Product FK in fact_sales
    orphan_products = set(sales["product_key"].dropna()) - set(products["product_key"])
    assert len(orphan_products) == 0, f"Found orphan product keys: {orphan_products}"
    
    # Seller FK in fact_sales
    orphan_sellers = set(sales["seller_key"].dropna()) - set(sellers["seller_key"])
    assert len(orphan_sellers) == 0, f"Found orphan seller keys: {orphan_sellers}"


def test_financial_ranges(datasets):
    """Verify prices and freight values are strictly non-negative."""
    sales = datasets["fact_sales"]
    payments = datasets["fact_payments"]
    
    assert (sales["price"] >= 0).all(), "Found negative price in fact_sales!"
    assert (sales["freight_value"] >= 0).all(), "Found negative freight in fact_sales!"
    assert (payments["payment_value"] >= 0).all(), "Found negative payment value in fact_payments!"


def test_review_score_ranges(datasets):
    """Verify customer ratings strictly adhere to 1-5 integer scale."""
    reviews = datasets["fact_reviews"]
    assert reviews["review_score"].between(1, 5).all(), "Found review scores outside 1-5 range!"


def test_delivered_orders_integrity(datasets):
    """Verify delivered orders have valid non-negative delivery duration."""
    orders = datasets["fact_orders"]
    delivered = orders[(orders["order_status"] == "delivered") & orders["delivery_days"].notna()]
    
    assert (delivered["delivery_days"] >= 0).all(), "Found negative delivery turnaround on delivered orders!"
    assert (delivered["is_late"].isin([0, 1])).all()

