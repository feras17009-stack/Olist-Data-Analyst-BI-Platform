-- ============================================================================
-- 08_analysis_queries.sql
-- In-Depth Business Intelligence Query Suite
-- Covers: Sales, Products, Customers, Geography, Logistics, Sellers, Reviews
-- ============================================================================

-- ============================================================================
-- SECTION 1: SALES & REVENUE ANALYSIS
-- ============================================================================

-- 1.1 Top 10 Best-Selling Product Categories by Revenue
SELECT
    COALESCE(p.product_category_name_english, 'Unknown') AS category_name,
    COUNT(DISTINCT s.order_id) AS total_orders,
    COUNT(s.sales_key) AS total_units_sold,
    ROUND(SUM(s.price), 2) AS product_revenue,
    ROUND(SUM(s.freight_value), 2) AS freight_revenue,
    ROUND(SUM(s.item_value), 2) AS total_revenue,
    ROUND(AVG(s.price), 2) AS avg_item_price
FROM analytics.fact_sales s
JOIN analytics.dim_product p ON s.product_key = p.product_key
GROUP BY 1
ORDER BY total_revenue DESC
LIMIT 10;

-- 1.2 Revenue and Order Growth by Year and Quarter
SELECT
    d.year,
    d.quarter_name,
    COUNT(DISTINCT s.order_id) AS total_orders,
    COUNT(s.sales_key) AS units_sold,
    ROUND(SUM(s.item_value), 2) AS total_revenue,
    ROUND(SUM(s.item_value) / NULLIF(COUNT(DISTINCT s.order_id), 0), 2) AS avg_order_value
FROM analytics.fact_sales s
JOIN analytics.dim_date d ON s.date_key = d.date_key
GROUP BY d.year, d.quarter_name
ORDER BY d.year, d.quarter_name;

-- 1.3 Day of Week & Hour Purchasing Patterns
SELECT
    d.day_name,
    COUNT(DISTINCT s.order_id) AS total_orders,
    ROUND(SUM(s.item_value), 2) AS total_revenue,
    ROUND(AVG(s.item_value), 2) AS avg_item_value
FROM analytics.fact_sales s
JOIN analytics.dim_date d ON s.date_key = d.date_key
GROUP BY d.day_name, d.day_of_week
ORDER BY d.day_of_week;


-- ============================================================================
-- SECTION 2: CUSTOMER ANALYTICS & RFM BEHAVIOR
-- ============================================================================

-- 2.1 Customer Retention: Repeat vs Single-Purchase Customers
SELECT
    CASE WHEN is_repeat_customer = 1 THEN 'Repeat Buyer (>1 Order)' ELSE 'Single Purchase (1 Order)' END AS customer_type,
    COUNT(DISTINCT customer_unique_id) AS unique_customers,
    ROUND(100.0 * COUNT(DISTINCT customer_unique_id) / SUM(COUNT(DISTINCT customer_unique_id)) OVER (), 2) AS pct_customers,
    ROUND(SUM(rfm_monetary), 2) AS total_revenue,
    ROUND(100.0 * SUM(rfm_monetary) / SUM(SUM(rfm_monetary)) OVER (), 2) AS pct_revenue,
    ROUND(AVG(rfm_monetary), 2) AS avg_revenue_per_customer
FROM analytics.dim_customer
GROUP BY 1;

-- 2.2 Top 10 High-Value Customers
SELECT
    customer_unique_id,
    customer_state,
    rfm_segment,
    rfm_frequency AS total_orders,
    rfm_monetary AS lifetime_spend,
    rfm_recency AS days_since_last_order
FROM analytics.dim_customer
ORDER BY rfm_monetary DESC
LIMIT 10;

-- 2.3 RFM Segment Performance Breakdown
SELECT
    rfm_segment,
    COUNT(DISTINCT customer_unique_id) AS total_customers,
    ROUND(SUM(rfm_monetary), 2) AS total_revenue,
    ROUND(AVG(rfm_monetary), 2) AS avg_customer_value,
    ROUND(AVG(rfm_recency), 1) AS avg_recency_days
FROM analytics.dim_customer
GROUP BY rfm_segment
ORDER BY total_revenue DESC;


-- ============================================================================
-- SECTION 3: GEOGRAPHIC & REGIONAL PERFORMANCE
-- ============================================================================

-- 3.1 State-Level Revenue, Volume and Freight Contribution
SELECT
    c.customer_state,
    COUNT(DISTINCT o.order_id) AS total_orders,
    COUNT(DISTINCT c.customer_unique_id) AS unique_customers,
    ROUND(SUM(s.price), 2) AS product_revenue,
    ROUND(SUM(s.freight_value), 2) AS freight_revenue,
    ROUND(SUM(s.item_value), 2) AS total_revenue,
    ROUND(SUM(s.item_value) / NULLIF(COUNT(DISTINCT o.order_id), 0), 2) AS state_aov,
    ROUND(AVG(o.delivery_days), 1) AS avg_delivery_days,
    ROUND(
        100.0 * COUNT(DISTINCT CASE WHEN o.is_late = 1 THEN o.order_id END) / 
        NULLIF(COUNT(DISTINCT o.order_id), 0), 
        2
    ) AS late_delivery_rate_pct
FROM analytics.fact_orders o
JOIN analytics.fact_sales s ON o.order_id = s.order_id
JOIN analytics.dim_customer c ON o.customer_key = c.customer_key
WHERE o.order_status = 'delivered'
GROUP BY c.customer_state
ORDER BY total_revenue DESC;


-- ============================================================================
-- SECTION 4: PAYMENT METHODS & FINANCING
-- ============================================================================

-- 4.1 Payment Type Share and Average Transaction Value
SELECT
    payment_type,
    COUNT(payment_key) AS transaction_count,
    ROUND(100.0 * COUNT(payment_key) / SUM(COUNT(payment_key)) OVER (), 2) AS pct_transactions,
    ROUND(SUM(payment_value), 2) AS total_payment_value,
    ROUND(100.0 * SUM(payment_value) / SUM(SUM(payment_value)) OVER (), 2) AS pct_value,
    ROUND(AVG(payment_value), 2) AS avg_transaction_value,
    ROUND(AVG(payment_installments), 1) AS avg_installments
FROM analytics.fact_payments
GROUP BY payment_type
ORDER BY total_payment_value DESC;


-- ============================================================================
-- SECTION 5: OPERATIONS, LOGISTICS & SELLER PERFORMANCE
-- ============================================================================

-- 5.1 On-Time vs Delayed Deliveries Impact on Review Scores
SELECT
    CASE 
        WHEN o.is_late = 1 THEN 'Delayed (Arrived After Estimated Date)'
        WHEN o.delivery_days <= o.estimated_delivery_days THEN 'On-Time / Early'
        ELSE 'Other'
    END AS delivery_performance,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(100.0 * COUNT(DISTINCT o.order_id) / SUM(COUNT(DISTINCT o.order_id)) OVER (), 2) AS pct_orders,
    ROUND(AVG(o.delivery_days), 1) AS avg_actual_delivery_days,
    ROUND(AVG(r.review_score), 2) AS avg_customer_review_score,
    ROUND(100.0 * COUNT(CASE WHEN r.review_score = 1 THEN 1 END) / COUNT(r.review_record_key), 2) AS pct_1_star_reviews,
    ROUND(100.0 * COUNT(CASE WHEN r.review_score = 5 THEN 1 END) / COUNT(r.review_record_key), 2) AS pct_5_star_reviews
FROM analytics.fact_orders o
LEFT JOIN analytics.fact_reviews r ON o.order_id = r.order_id
WHERE o.order_status = 'delivered'
GROUP BY 1;

-- 5.2 Top 10 Sellers by Revenue and Their Quality Metrics
SELECT
    sel.seller_id,
    sel.seller_state,
    COUNT(DISTINCT s.order_id) AS total_orders,
    COUNT(s.sales_key) AS units_sold,
    ROUND(SUM(s.item_value), 2) AS total_revenue,
    ROUND(AVG(r.review_score), 2) AS avg_review_score,
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN o.is_late = 1 THEN o.order_id END) / NULLIF(COUNT(DISTINCT o.order_id), 0), 2) AS seller_late_pct
FROM analytics.fact_sales s
JOIN analytics.dim_seller sel ON s.seller_key = sel.seller_key
JOIN analytics.fact_orders o ON s.order_id = o.order_id
LEFT JOIN analytics.fact_reviews r ON s.order_id = r.order_id
GROUP BY sel.seller_id, sel.seller_state
ORDER BY total_revenue DESC
LIMIT 10;
