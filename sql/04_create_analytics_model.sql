-- ============================================================================
-- 04_create_analytics_model.sql
-- Dimensional Star Schema Layer (Analytics Model) for Power BI and SQL Queries
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Dimension 1: dim_date
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS analytics.dim_date CASCADE;
CREATE TABLE analytics.dim_date (
    date_key INT PRIMARY KEY,
    full_date DATE NOT NULL,
    year INT NOT NULL,
    quarter INT NOT NULL,
    quarter_name VARCHAR(20) NOT NULL,
    month INT NOT NULL,
    month_name VARCHAR(20) NOT NULL,
    year_month VARCHAR(10) NOT NULL,
    week INT NOT NULL,
    day INT NOT NULL,
    day_of_week INT NOT NULL,
    day_name VARCHAR(20) NOT NULL,
    is_weekend INT NOT NULL,
    is_month_end INT NOT NULL
);

-- ----------------------------------------------------------------------------
-- Dimension 2: dim_customer
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS analytics.dim_customer CASCADE;
CREATE TABLE analytics.dim_customer (
    customer_key INT PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL UNIQUE,
    customer_unique_id VARCHAR(50) NOT NULL,
    customer_zip_code_prefix INT,
    customer_city VARCHAR(100),
    customer_state VARCHAR(5),
    rfm_recency INT,
    rfm_frequency INT,
    rfm_monetary NUMERIC(12, 2),
    rfm_segment VARCHAR(50),
    is_repeat_customer INT
);

-- ----------------------------------------------------------------------------
-- Dimension 3: dim_product
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS analytics.dim_product CASCADE;
CREATE TABLE analytics.dim_product (
    product_key INT PRIMARY KEY,
    product_id VARCHAR(50) NOT NULL UNIQUE,
    product_category_name VARCHAR(100),
    product_category_name_english VARCHAR(100),
    product_name_length INT,
    product_description_length INT,
    product_photos_qty INT,
    product_weight_g NUMERIC(10, 2),
    product_length_cm NUMERIC(10, 2),
    product_height_cm NUMERIC(10, 2),
    product_width_cm NUMERIC(10, 2)
);

-- ----------------------------------------------------------------------------
-- Dimension 4: dim_seller
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS analytics.dim_seller CASCADE;
CREATE TABLE analytics.dim_seller (
    seller_key INT PRIMARY KEY,
    seller_id VARCHAR(50) NOT NULL UNIQUE,
    seller_zip_code_prefix INT,
    seller_city VARCHAR(100),
    seller_state VARCHAR(5)
);

-- ----------------------------------------------------------------------------
-- Dimension 5: dim_location
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS analytics.dim_location CASCADE;
CREATE TABLE analytics.dim_location (
    location_key INT PRIMARY KEY,
    geolocation_zip_code_prefix INT,
    latitude NUMERIC(9, 6),
    longitude NUMERIC(9, 6),
    city VARCHAR(100),
    state VARCHAR(5)
);

-- ----------------------------------------------------------------------------
-- Fact 1: fact_orders (Grain: One row per order)
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS analytics.fact_orders CASCADE;
CREATE TABLE analytics.fact_orders (
    order_key INT PRIMARY KEY,
    order_id VARCHAR(50) NOT NULL UNIQUE,
    customer_key INT REFERENCES analytics.dim_customer(customer_key),
    customer_id VARCHAR(50),
    order_status VARCHAR(30),
    purchase_date_key INT REFERENCES analytics.dim_date(date_key),
    order_purchase_timestamp TIMESTAMP,
    order_approved_at TIMESTAMP,
    order_delivered_carrier_date TIMESTAMP,
    order_delivered_customer_date TIMESTAMP,
    order_estimated_delivery_date TIMESTAMP,
    delivery_days NUMERIC(10, 2),
    estimated_delivery_days NUMERIC(10, 2),
    delay_days NUMERIC(10, 2),
    is_delivered INT,
    is_late INT,
    order_item_count INT,
    total_order_value NUMERIC(12, 2),
    total_freight_value NUMERIC(12, 2),
    total_order_amount NUMERIC(12, 2)
);

-- ----------------------------------------------------------------------------
-- Fact 2: fact_sales (Grain: One row per order item)
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS analytics.fact_sales CASCADE;
CREATE TABLE analytics.fact_sales (
    sales_key INT PRIMARY KEY,
    order_id VARCHAR(50) NOT NULL,
    order_item_id INT NOT NULL,
    customer_key INT REFERENCES analytics.dim_customer(customer_key),
    product_key INT REFERENCES analytics.dim_product(product_key),
    seller_key INT REFERENCES analytics.dim_seller(seller_key),
    date_key INT REFERENCES analytics.dim_date(date_key),
    order_status VARCHAR(30),
    price NUMERIC(10, 2) NOT NULL,
    freight_value NUMERIC(10, 2) NOT NULL,
    item_value NUMERIC(10, 2) NOT NULL
);

-- ----------------------------------------------------------------------------
-- Fact 3: fact_payments (Grain: One payment installment/transaction)
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS analytics.fact_payments CASCADE;
CREATE TABLE analytics.fact_payments (
    payment_key INT PRIMARY KEY,
    order_id VARCHAR(50) NOT NULL,
    payment_sequential INT NOT NULL,
    payment_type VARCHAR(30) NOT NULL,
    payment_installments INT NOT NULL,
    payment_value NUMERIC(10, 2) NOT NULL,
    date_key INT REFERENCES analytics.dim_date(date_key)
);

-- ----------------------------------------------------------------------------
-- Fact 4: fact_reviews (Grain: One review submission)
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS analytics.fact_reviews CASCADE;
CREATE TABLE analytics.fact_reviews (
    review_record_key INT PRIMARY KEY,
    review_id VARCHAR(50) NOT NULL,
    order_id VARCHAR(50) NOT NULL,
    review_score INT NOT NULL CHECK (review_score BETWEEN 1 AND 5),
    has_comment INT NOT NULL,
    review_creation_date TIMESTAMP,
    review_answer_timestamp TIMESTAMP,
    date_key INT REFERENCES analytics.dim_date(date_key)
);
