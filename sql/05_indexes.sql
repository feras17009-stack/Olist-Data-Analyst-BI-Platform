-- ============================================================================
-- 05_indexes.sql
-- Performance Optimization Indexes for PostgreSQL / Analytical Queries
-- ============================================================================

-- Date Dimension Indexes
CREATE INDEX IF NOT EXISTS idx_dim_date_year ON analytics.dim_date(year);
CREATE INDEX IF NOT EXISTS idx_dim_date_year_month ON analytics.dim_date(year_month);

-- Customer Dimension Indexes
CREATE INDEX IF NOT EXISTS idx_dim_customer_unique_id ON analytics.dim_customer(customer_unique_id);
CREATE INDEX IF NOT EXISTS idx_dim_customer_state ON analytics.dim_customer(customer_state);
CREATE INDEX IF NOT EXISTS idx_dim_customer_segment ON analytics.dim_customer(rfm_segment);

-- Product Dimension Indexes
CREATE INDEX IF NOT EXISTS idx_dim_product_category ON analytics.dim_product(product_category_name_english);

-- Seller Dimension Indexes
CREATE INDEX IF NOT EXISTS idx_dim_seller_state ON analytics.dim_seller(seller_state);

-- Fact Orders Indexes
CREATE INDEX IF NOT EXISTS idx_fact_orders_customer_key ON analytics.fact_orders(customer_key);
CREATE INDEX IF NOT EXISTS idx_fact_orders_purchase_date_key ON analytics.fact_orders(purchase_date_key);
CREATE INDEX IF NOT EXISTS idx_fact_orders_status ON analytics.fact_orders(order_status);
CREATE INDEX IF NOT EXISTS idx_fact_orders_is_late ON analytics.fact_orders(is_late);

-- Fact Sales Indexes
CREATE INDEX IF NOT EXISTS idx_fact_sales_order_id ON analytics.fact_sales(order_id);
CREATE INDEX IF NOT EXISTS idx_fact_sales_customer_key ON analytics.fact_sales(customer_key);
CREATE INDEX IF NOT EXISTS idx_fact_sales_product_key ON analytics.fact_sales(product_key);
CREATE INDEX IF NOT EXISTS idx_fact_sales_seller_key ON analytics.fact_sales(seller_key);
CREATE INDEX IF NOT EXISTS idx_fact_sales_date_key ON analytics.fact_sales(date_key);

-- Fact Payments Indexes
CREATE INDEX IF NOT EXISTS idx_fact_payments_order_id ON analytics.fact_payments(order_id);
CREATE INDEX IF NOT EXISTS idx_fact_payments_type ON analytics.fact_payments(payment_type);

-- Fact Reviews Indexes
CREATE INDEX IF NOT EXISTS idx_fact_reviews_order_id ON analytics.fact_reviews(order_id);
CREATE INDEX IF NOT EXISTS idx_fact_reviews_score ON analytics.fact_reviews(review_score);
