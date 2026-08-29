# Data Dictionary — Olist E-Commerce Analytics Platform

This document details every table and column across the **Source Data Layer**, **Staging Layer**, and **Analytics Dimensional Star Schema Layer**.

---

## 1. Dimensional Model (Analytics Layer)

### `analytics.dim_date`
Calendar dimension providing standard temporal hierarchies.

| Column | Type | Nullable | Primary/Foreign Key | Description | Business Context |
|---|---|---|---|---|---|
| `date_key` | INT | No | Primary Key | Date in `YYYYMMDD` integer format | Used as surrogate key for joining fact tables |
| `full_date` | DATE | No | | Gregorian calendar date | Standard calendar reference |
| `year` | INT | No | | 4-digit calendar year (e.g. 2017, 2018) | Annual aggregation |
| `quarter` | INT | No | | Calendar quarter (1–4) | Quarterly pacing & growth analysis |
| `quarter_name` | VARCHAR | No | | Formatted quarter (e.g. 'Q1 2018') | Visual label in BI reports |
| `month` | INT | No | | Calendar month (1–12) | Monthly reporting |
| `month_name` | VARCHAR | No | | Full month name (e.g. 'January') | Slicing and dashboard labels |
| `year_month` | VARCHAR | No | | Formatted year-month `YYYY-MM` | Time-series continuous trends |
| `week` | INT | No | | ISO calendar week number (1–53) | Weekly performance tracking |
| `day` | INT | No | | Day of the month (1–31) | Daily granularity |
| `day_of_week` | INT | No | | Day of week (1=Monday, 7=Sunday) | Day of week purchasing habits |
| `day_name` | VARCHAR | No | | Full day name (e.g. 'Monday') | Weekday vs weekend analysis |
| `is_weekend` | INT | No | | 1 if Saturday/Sunday, 0 if weekday | Weekend shopper behavior flag |
| `is_month_end` | INT | No | | 1 if last day of the month | Payday / end-of-month surges |

---

### `analytics.dim_customer`
Customer dimension with geographical attributes and computed RFM behavioral segmentation.

| Column | Type | Nullable | Primary/Foreign Key | Description | Business Context |
|---|---|---|---|---|---|
| `customer_key` | INT | No | Primary Key | Surrogate integer key | Fast joins in star schema |
| `customer_id` | VARCHAR(50) | No | Unique | Olist transactional customer key | Unique per individual transaction |
| `customer_unique_id` | VARCHAR(50) | No | | Persistent individual identifier | Identifies true unique customer across multiple purchases |
| `customer_zip_code_prefix` | INT | Yes | | Brazilian postal code prefix (5 digits) | Geospatial grouping |
| `customer_city` | VARCHAR(100) | Yes | | City name | Metropolitan demand analysis |
| `customer_state` | VARCHAR(5) | Yes | | 2-letter state code (e.g. 'SP', 'RJ') | State-level logistics & marketing targeting |
| `rfm_recency` | INT | Yes | | Days since most recent purchase | Recency score component |
| `rfm_frequency` | INT | Yes | | Total number of lifetime orders | Customer loyalty metric |
| `rfm_monetary` | NUMERIC(12,2) | Yes | | Total gross spend (BRL) | Customer Lifetime Value (CLV) |
| `rfm_segment` | VARCHAR(50) | Yes | | RFM segment label | Categorization (e.g. 'Champions', 'At Risk') |
| `is_repeat_customer` | INT | No | | 1 if frequency > 1, 0 otherwise | Direct retention cohort flag |

---

### `analytics.dim_product`
Product catalog dimension enriched with English translations and physical attributes.

| Column | Type | Nullable | Primary/Foreign Key | Description | Business Context |
|---|---|---|---|---|---|
| `product_key` | INT | No | Primary Key | Surrogate integer key | Fact table join key |
| `product_id` | VARCHAR(50) | No | Unique | Natural product hash identifier | Unique SKU identifier |
| `product_category_name` | VARCHAR(100) | Yes | | Original Portuguese category name | Source category name |
| `product_category_name_english` | VARCHAR(100) | Yes | | Standardized English category name | Main category grouping in reports |
| `product_name_length` | INT | Yes | | Character count of product title | Listing optimization attribute |
| `product_description_length` | INT | Yes | | Character count of product description | Listing completeness metric |
| `product_photos_qty` | INT | Yes | | Number of published product photos | Media quality indicator |
| `product_weight_g` | NUMERIC(10,2) | Yes | | Weight in grams | Freight and logistics calculation |
| `product_length_cm` | NUMERIC(10,2) | Yes | | Length in centimeters | Package dimensional sizing |
| `product_height_cm` | NUMERIC(10,2) | Yes | | Height in centimeters | Packaging constraints |
| `product_width_cm` | NUMERIC(10,2) | Yes | | Width in centimeters | Volume calculations |

---

### `analytics.dim_seller`
Merchant / Seller dimension with geographic origins.

| Column | Type | Nullable | Primary/Foreign Key | Description | Business Context |
|---|---|---|---|---|---|
| `seller_key` | INT | No | Primary Key | Surrogate integer key | Fact table join key |
| `seller_id` | VARCHAR(50) | No | Unique | Natural seller hash identifier | Marketplace vendor ID |
| `seller_zip_code_prefix` | INT | Yes | | Seller postal code prefix | Origin location for fulfillment |
| `seller_city` | VARCHAR(100) | Yes | | Seller registered city | Regional supply cluster |
| `seller_state` | VARCHAR(5) | Yes | | Seller registered state code | Regional logistics corridor analysis |

---

### `analytics.dim_location`
Geospatial master dimension aggregated by Brazilian postal code prefixes.

| Column | Type | Nullable | Primary/Foreign Key | Description | Business Context |
|---|---|---|---|---|---|
| `location_key` | INT | No | Primary Key | Surrogate integer key | Geographical lookup key |
| `geolocation_zip_code_prefix`| INT | No | | 5-digit postal code prefix | Regional zip cluster |
| `latitude` | NUMERIC(9,6) | No | | Median GPS latitude | Mapping / GIS visualization |
| `longitude` | NUMERIC(9,6) | No | | Median GPS longitude | Mapping / GIS visualization |
| `city` | VARCHAR(100) | Yes | | Modal city name for zip code | City label |
| `state` | VARCHAR(5) | Yes | | Brazilian state code | State label |

---

### `analytics.fact_orders`
Order-level grain fact table containing order fulfillment lifecycles and delivery SLA metrics.

| Column | Type | Nullable | Primary/Foreign Key | Description | Business Context |
|---|---|---|---|---|---|
| `order_key` | INT | No | Primary Key | Surrogate order key | Order identifier |
| `order_id` | VARCHAR(50) | No | Unique | Natural order identifier | Order reference |
| `customer_key` | INT | Yes | FK -> `dim_customer` | Customer dimension reference | Identifies the ordering customer |
| `purchase_date_key` | INT | Yes | FK -> `dim_date` | Purchase date key (`YYYYMMDD`) | Primary temporal join key |
| `order_status` | VARCHAR(30) | No | | Status (`delivered`, `canceled`, etc.) | Order conversion funnel |
| `order_purchase_timestamp` | TIMESTAMP | No | | Timestamp when customer placed order | Baseline order timestamp |
| `order_approved_at` | TIMESTAMP | Yes | | Payment approval timestamp | Payment processing latency |
| `order_delivered_carrier_date` | TIMESTAMP | Yes | | Handover timestamp to carrier | Seller fulfillment SLA |
| `order_delivered_customer_date` | TIMESTAMP | Yes | | Final delivery timestamp | Customer receipt timestamp |
| `order_estimated_delivery_date` | TIMESTAMP | No | | Quoted estimated delivery date | Customer promise SLA date |
| `delivery_days` | NUMERIC(10,2) | Yes | | Days from purchase to delivery | Total delivery turnaround time |
| `estimated_delivery_days` | NUMERIC(10,2) | Yes | | Days from purchase to estimate | Quoted delivery window |
| `delay_days` | NUMERIC(10,2) | Yes | | Days delivered past estimate | Delivery delay (>0 means late) |
| `is_delivered` | INT | No | | 1 if delivered, 0 otherwise | Delivered order flag |
| `is_late` | INT | No | | 1 if delivered after estimate, 0 otherwise | Logistics SLA breach indicator |
| `order_item_count` | INT | No | | Number of distinct items in order | Basket size |
| `total_order_value` | NUMERIC(12,2) | No | | Total item price sum (BRL) | Product GMV |
| `total_freight_value` | NUMERIC(12,2) | No | | Total freight charged (BRL) | Shipping revenue |
| `total_order_amount` | NUMERIC(12,2) | No | | Sum of item prices + freight | Total invoice value |

---

### `analytics.fact_sales`
Order item-level grain fact table representing individual SKU sale transactions.

| Column | Type | Nullable | Primary/Foreign Key | Description | Business Context |
|---|---|---|---|---|---|
| `sales_key` | INT | No | Primary Key | Surrogate sales item key | Unique item sale identifier |
| `order_id` | VARCHAR(50) | No | | Natural order identifier | Links to parent order |
| `order_item_id` | INT | No | | Item sequence within order (1, 2...) | Item index |
| `customer_key` | INT | Yes | FK -> `dim_customer` | Customer dimension reference | Customer demographic link |
| `product_key` | INT | Yes | FK -> `dim_product` | Product dimension reference | Product taxonomy link |
| `seller_key` | INT | Yes | FK -> `dim_seller` | Seller dimension reference | Vendor attribution link |
| `date_key` | INT | Yes | FK -> `dim_date` | Purchase date key | Calendar link |
| `order_status` | VARCHAR(30) | No | | Status of the parent order | Sales validation status |
| `price` | NUMERIC(10,2) | No | | Item product price (BRL) | Core product revenue |
| `freight_value` | NUMERIC(10,2) | No | | Item freight charge (BRL) | Freight fee allocated |
| `item_value` | NUMERIC(10,2) | No | | Total item value (`price + freight`) | Total line item revenue |

---

### `analytics.fact_payments`
Payment transaction grain fact table.

| Column | Type | Nullable | Primary/Foreign Key | Description | Business Context |
|---|---|---|---|---|---|
| `payment_key` | INT | No | Primary Key | Surrogate payment transaction key | Unique payment record |
| `order_id` | VARCHAR(50) | No | | Natural order identifier | Link to order |
| `payment_sequential` | INT | No | | Sequence index of payment | Split-tender sequence |
| `payment_type` | VARCHAR(30) | No | | Method (`credit_card`, `boleto`, etc.) | Payment channel share |
| `payment_installments` | INT | No | | Number of financing installments | Financing behavior (1–24x) |
| `payment_value` | NUMERIC(10,2) | No | | Transaction value in BRL | Cashflow settlement |
| `date_key` | INT | Yes | FK -> `dim_date` | Order purchase date key | Payment timing |

---

### `analytics.fact_reviews`
Customer review survey grain fact table.

| Column | Type | Nullable | Primary/Foreign Key | Description | Business Context |
|---|---|---|---|---|---|
| `review_record_key` | INT | No | Primary Key | Surrogate review key | Review record identifier |
| `review_id` | VARCHAR(50) | No | | Natural review identifier | Review submission ID |
| `order_id` | VARCHAR(50) | No | | Associated order identifier | Order link |
| `review_score` | INT | No | | Customer rating (1 to 5 stars) | Customer satisfaction CSAT score |
| `has_comment` | INT | No | | 1 if comment/title provided, 0 if score only | Qualitative feedback presence |
| `review_creation_date` | TIMESTAMP | Yes | | Survey invitation creation timestamp | Feedback solicitation date |
| `review_answer_timestamp` | TIMESTAMP | Yes | | Customer response timestamp | Feedback turnaround speed |
| `date_key` | INT | Yes | FK -> `dim_date` | Order purchase date key | Review cohort date |
