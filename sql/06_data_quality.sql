-- ============================================================================
-- 06_data_quality.sql
-- Automated Data Quality & Integrity Validation Queries
-- Checks Uniqueness, Nulls, Referential Integrity, Financial Validity & Dates
-- ============================================================================

-- ----------------------------------------------------------------------------
-- 1. Uniqueness Checks
-- ----------------------------------------------------------------------------
-- Duplicate Order IDs in Orders Table (Expect 0)
SELECT 'Duplicate Orders' AS test_name, COUNT(*) AS failed_records
FROM (
    SELECT order_id FROM analytics.fact_orders GROUP BY order_id HAVING COUNT(*) > 1
) sub;

-- Duplicate Products (Expect 0)
SELECT 'Duplicate Products' AS test_name, COUNT(*) AS failed_records
FROM (
    SELECT product_id FROM analytics.dim_product GROUP BY product_id HAVING COUNT(*) > 1
) sub;

-- Duplicate Sellers (Expect 0)
SELECT 'Duplicate Sellers' AS test_name, COUNT(*) AS failed_records
FROM (
    SELECT seller_id FROM analytics.dim_seller GROUP BY seller_id HAVING COUNT(*) > 1
) sub;


-- ----------------------------------------------------------------------------
-- 2. Referential Integrity Checks (Orphan Records)
-- ----------------------------------------------------------------------------
-- Fact Sales items without matching order in Fact Orders (Expect 0)
SELECT 'Orphan Sales Items (No Order)' AS test_name, COUNT(*) AS failed_records
FROM analytics.fact_sales s
LEFT JOIN analytics.fact_orders o ON s.order_id = o.order_id
WHERE o.order_id IS NULL;

-- Fact Sales items without matching product in Dim Product (Expect 0)
SELECT 'Orphan Sales Items (No Product)' AS test_name, COUNT(*) AS failed_records
FROM analytics.fact_sales s
LEFT JOIN analytics.dim_product p ON s.product_key = p.product_key
WHERE p.product_key IS NULL;

-- Fact Sales items without matching seller in Dim Seller (Expect 0)
SELECT 'Orphan Sales Items (No Seller)' AS test_name, COUNT(*) AS failed_records
FROM analytics.fact_sales s
LEFT JOIN analytics.dim_seller sel ON s.seller_key = sel.seller_key
WHERE sel.seller_key IS NULL;

-- Fact Payments without matching order (Expect 0)
SELECT 'Orphan Payments (No Order)' AS test_name, COUNT(*) AS failed_records
FROM analytics.fact_payments p
LEFT JOIN analytics.fact_orders o ON p.order_id = o.order_id
WHERE o.order_id IS NULL;


-- ----------------------------------------------------------------------------
-- 3. Value Range & Financial Validity Checks
-- ----------------------------------------------------------------------------
-- Negative Item Price (Expect 0)
SELECT 'Negative Price Check' AS test_name, COUNT(*) AS failed_records
FROM analytics.fact_sales
WHERE price < 0;

-- Negative Freight Value (Expect 0)
SELECT 'Negative Freight Check' AS test_name, COUNT(*) AS failed_records
FROM analytics.fact_sales
WHERE freight_value < 0;

-- Invalid Review Score (Expect 0)
SELECT 'Invalid Review Score Check' AS test_name, COUNT(*) AS failed_records
FROM analytics.fact_reviews
WHERE review_score NOT BETWEEN 1 AND 5;


-- ----------------------------------------------------------------------------
-- 4. Temporal / Date Consistency Checks
-- ----------------------------------------------------------------------------
-- Delivered Date before Purchase Date (Expect 0)
SELECT 'Delivered Before Purchase' AS test_name, COUNT(*) AS failed_records
FROM analytics.fact_orders
WHERE order_delivered_customer_date < order_purchase_timestamp;

-- Order Approval before Purchase Date (Expect 0)
SELECT 'Approved Before Purchase' AS test_name, COUNT(*) AS failed_records
FROM analytics.fact_orders
WHERE order_approved_at < order_purchase_timestamp;
