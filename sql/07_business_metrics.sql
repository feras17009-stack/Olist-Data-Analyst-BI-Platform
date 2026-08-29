-- ============================================================================
-- 07_business_metrics.sql
-- Core Business KPIs, Views and Aggregated Metrics
-- ============================================================================

-- ----------------------------------------------------------------------------
-- View 1: Executive KPI Summary
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW analytics.vw_executive_kpis AS
SELECT
    COUNT(DISTINCT o.order_id) AS total_orders,
    COUNT(DISTINCT CASE WHEN o.order_status = 'delivered' THEN o.order_id END) AS delivered_orders,
    COUNT(DISTINCT c.customer_unique_id) AS total_customers,
    ROUND(SUM(s.price), 2) AS total_product_revenue,
    ROUND(SUM(s.freight_value), 2) AS total_freight_revenue,
    ROUND(SUM(s.item_value), 2) AS total_revenue,
    ROUND(SUM(s.item_value) / NULLIF(COUNT(DISTINCT o.order_id), 0), 2) AS average_order_value,
    ROUND(COUNT(s.sales_key)::NUMERIC / NULLIF(COUNT(DISTINCT o.order_id), 0), 2) AS items_per_order,
    ROUND(AVG(CASE WHEN o.order_status = 'delivered' THEN o.delivery_days END), 1) AS avg_delivery_days,
    ROUND(
        100.0 * COUNT(DISTINCT CASE WHEN o.order_status = 'delivered' AND o.is_late = 1 THEN o.order_id END) / 
        NULLIF(COUNT(DISTINCT CASE WHEN o.order_status = 'delivered' THEN o.order_id END), 0), 
        2
    ) AS late_delivery_rate_pct,
    ROUND(
        100.0 * COUNT(DISTINCT CASE WHEN c.is_repeat_customer = 1 THEN c.customer_unique_id END) / 
        NULLIF(COUNT(DISTINCT c.customer_unique_id), 0), 
        2
    ) AS repeat_customer_rate_pct
FROM analytics.fact_orders o
JOIN analytics.fact_sales s ON o.order_id = s.order_id
JOIN analytics.dim_customer c ON o.customer_key = c.customer_key;


-- ----------------------------------------------------------------------------
-- View 2: Monthly Financial Performance & Growth (MoM)
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW analytics.vw_monthly_sales_trend AS
WITH monthly_metrics AS (
    SELECT
        d.year,
        d.month,
        d.year_month,
        COUNT(DISTINCT s.order_id) AS orders_count,
        COUNT(s.sales_key) AS items_sold_count,
        ROUND(SUM(s.price), 2) AS product_revenue,
        ROUND(SUM(s.freight_value), 2) AS freight_revenue,
        ROUND(SUM(s.item_value), 2) AS total_revenue,
        ROUND(SUM(s.item_value) / NULLIF(COUNT(DISTINCT s.order_id), 0), 2) AS monthly_aov
    FROM analytics.fact_sales s
    JOIN analytics.dim_date d ON s.date_key = d.date_key
    GROUP BY d.year, d.month, d.year_month
)
SELECT
    year,
    month,
    year_month,
    orders_count,
    items_sold_count,
    product_revenue,
    freight_revenue,
    total_revenue,
    monthly_aov,
    LAG(total_revenue) OVER (ORDER BY year, month) AS prev_month_revenue,
    ROUND(
        100.0 * (total_revenue - LAG(total_revenue) OVER (ORDER BY year, month)) / 
        NULLIF(LAG(total_revenue) OVER (ORDER BY year, month), 0), 
        2
    ) AS mom_revenue_growth_pct
FROM monthly_metrics
ORDER BY year, month;


-- ----------------------------------------------------------------------------
-- View 3: Customer RFM Segment Distribution
-- ----------------------------------------------------------------------------
CREATE OR REPLACE VIEW analytics.vw_rfm_segment_summary AS
SELECT
    rfm_segment,
    COUNT(DISTINCT customer_unique_id) AS customer_count,
    ROUND(100.0 * COUNT(DISTINCT customer_unique_id) / SUM(COUNT(DISTINCT customer_unique_id)) OVER (), 2) AS customer_pct,
    ROUND(SUM(rfm_monetary), 2) AS total_segment_revenue,
    ROUND(100.0 * SUM(rfm_monetary) / SUM(SUM(rfm_monetary)) OVER (), 2) AS revenue_pct,
    ROUND(AVG(rfm_recency), 1) AS avg_recency_days,
    ROUND(AVG(rfm_frequency), 2) AS avg_frequency,
    ROUND(AVG(rfm_monetary), 2) AS avg_monetary_per_customer
FROM analytics.dim_customer
GROUP BY rfm_segment
ORDER BY total_segment_revenue DESC;
