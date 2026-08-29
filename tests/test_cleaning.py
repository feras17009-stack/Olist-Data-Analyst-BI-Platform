"""
Unit tests for data cleaning and standardization functions.
"""

import pytest
import pandas as pd
import numpy as np
from src.data_cleaning import (
    to_snake_case,
    clean_column_names,
    clean_customers,
    clean_order_items,
    clean_order_payments,
    clean_order_reviews
)


def test_to_snake_case():
    assert to_snake_case("Order Purchase Timestamp") == "order_purchase_timestamp"
    assert to_snake_case("product_id") == "product_id"
    assert to_snake_case("Customer-Unique-ID") == "customer_unique_id"
    assert to_snake_case("  Total Value  ") == "total_value"


def test_clean_customers():
    raw_df = pd.DataFrame({
        "Customer ID": ["c1", "c1"],
        "Customer Unique ID": ["u1", "u1"],
        "Customer Zip Code Prefix": ["01310", "01310"],
        "Customer City": ["sao paulo", "sao paulo"],
        "Customer State": ["sp", "sp"]
    })
    cleaned = clean_customers(raw_df)
    assert len(cleaned) == 1
    assert cleaned.iloc[0]["customer_city"] == "Sao Paulo"
    assert cleaned.iloc[0]["customer_state"] == "SP"
    assert cleaned.iloc[0]["customer_zip_code_prefix"] == 1310


def test_clean_order_items():
    raw_df = pd.DataFrame({
        "order_id": ["o1", "o1", "o2"],
        "order_item_id": [1, 1, 1],  # Duplicate item in o1
        "product_id": ["p1", "p1", "p2"],
        "seller_id": ["s1", "s1", "s2"],
        "price": [100.0, 100.0, -10.0],  # Negative price in o2
        "freight_value": [15.0, 15.0, 5.0]
    })
    cleaned = clean_order_items(raw_df)
    assert len(cleaned) == 1  # Deduplicates o1 and drops negative price o2
    assert cleaned.iloc[0]["order_id"] == "o1"
    assert cleaned.iloc[0]["price"] == 100.0


def test_clean_order_reviews():
    raw_df = pd.DataFrame({
        "review_id": ["r1", "r2"],
        "order_id": ["o1", "o2"],
        "review_score": [5, 6],  # 6 is invalid
        "review_comment_title": [None, "Great"],
        "review_comment_message": ["Good", "Super"],
        "review_creation_date": ["2018-01-01", "2018-01-02"],
        "review_answer_timestamp": ["2018-01-02", "2018-01-03"]
    })
    cleaned = clean_order_reviews(raw_df)
    assert len(cleaned) == 1
    assert cleaned.iloc[0]["review_id"] == "r1"
    assert cleaned.iloc[0]["review_score"] == 5
