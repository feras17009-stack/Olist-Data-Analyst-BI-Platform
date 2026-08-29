"""
Unit tests for feature engineering, delivery calculations, and RFM segmentation.
"""

import pytest
import pandas as pd
import numpy as np
from src.feature_engineering import (
    create_date_dimension,
    engineer_delivery_features,
    calculate_rfm_segments
)


def test_create_date_dimension():
    dim_date = create_date_dimension("2018-01-01", "2018-01-10")
    assert len(dim_date) == 10
    assert "date_key" in dim_date.columns
    assert "year_month" in dim_date.columns
    assert dim_date.iloc[0]["date_key"] == 20180101
    assert dim_date.iloc[0]["year"] == 2018
    assert dim_date.iloc[0]["month"] == 1


def test_engineer_delivery_features():
    orders = pd.DataFrame({
        "order_id": ["o1", "o2"],
        "order_status": ["delivered", "delivered"],
        "order_purchase_timestamp": pd.to_datetime(["2018-01-01 10:00:00", "2018-01-01 10:00:00"]),
        "order_delivered_customer_date": pd.to_datetime(["2018-01-05 10:00:00", "2018-01-15 10:00:00"]),
        "order_estimated_delivery_date": pd.to_datetime(["2018-01-10 10:00:00", "2018-01-10 10:00:00"])
    })
    
    fe_orders = engineer_delivery_features(orders)
    assert fe_orders.iloc[0]["delivery_days"] == pytest.approx(4.0, 0.01)
    assert fe_orders.iloc[0]["is_late"] == 0  # Delivered on 5th vs estimated 10th
    
    assert fe_orders.iloc[1]["delivery_days"] == pytest.approx(14.0, 0.01)
    assert fe_orders.iloc[1]["is_late"] == 1  # Delivered on 15th vs estimated 10th
    assert fe_orders.iloc[1]["delay_days"] == pytest.approx(5.0, 0.01)


def test_calculate_rfm_segments():
    customers = pd.DataFrame({
        "customer_id": ["c1", "c2", "c3", "c4"],
        "customer_unique_id": ["u1", "u1", "u2", "u3"]
    })
    orders = pd.DataFrame({
        "order_id": ["o1", "o2", "o3", "o4"],
        "customer_id": ["c1", "c2", "c3", "c4"],
        "order_status": ["delivered", "delivered", "delivered", "delivered"],
        "order_purchase_timestamp": pd.to_datetime([
            "2018-08-01", "2018-08-15", "2018-01-01", "2017-01-01"
        ])
    })
    items = pd.DataFrame({
        "order_id": ["o1", "o2", "o3", "o4"],
        "price": [100.0, 200.0, 50.0, 20.0],
        "freight_value": [10.0, 20.0, 10.0, 5.0]
    })
    
    rfm = calculate_rfm_segments(customers, orders, items)
    assert len(rfm) == 3  # 3 unique customers (u1, u2, u3)
    
    u1 = rfm[rfm["customer_unique_id"] == "u1"].iloc[0]
    assert u1["frequency"] == 2
    assert u1["is_repeat_customer"] == 1
    assert u1["monetary"] == 330.0
