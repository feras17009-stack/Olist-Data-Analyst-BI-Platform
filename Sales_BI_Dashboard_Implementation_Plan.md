# Sales & Business Intelligence Dashboard
## End-to-End E-Commerce Analytics Platform

## 1. Project Overview

**Project Name:** Sales & Business Intelligence Dashboard  
**Project Type:** End-to-End Data Analytics / Business Intelligence Project  
**Business Domain:** E-Commerce

### Primary Dataset

**Brazilian E-Commerce Public Dataset by Olist**

The Olist dataset contains approximately 100,000 orders from 2016–2018 and provides information across orders, customers, products, sellers, payments, freight, reviews, and geolocation.

### Project Goal

Build a complete analytics solution that transforms raw e-commerce data into actionable business intelligence.

```text
Raw Data
   ↓
Data Understanding
   ↓
Data Cleaning
   ↓
Data Validation
   ↓
Data Modeling
   ↓
PostgreSQL
   ↓
SQL Analytics
   ↓
Business Metrics
   ↓
Power BI
   ↓
Business Insights
   ↓
Recommendations
```

---

## 2. Business Problem

Assume that we are working as Data Analysts for an e-commerce company.

Management needs answers to:

### Sales
- How much revenue is being generated?
- How are sales changing over time?
- What months have the highest sales?
- What is the average order value?
- How many orders are completed, canceled, or unavailable?

### Products
- Which categories generate the most revenue?
- Which products sell the most?
- Which categories are growing?
- Which categories have poor customer satisfaction?

### Customers
- How many unique customers exist?
- How many customers purchase more than once?
- What is the average revenue per customer?
- Who are the highest-value customers?
- Which customer segments generate the most revenue?

### Geography
- Which states generate the most revenue?
- Where are customers concentrated?
- Which regions have the highest order volume?
- Which regions have poor delivery performance?

### Operations
- How long do orders take to arrive?
- What percentage of orders arrive late?
- Which sellers have poor delivery performance?
- Does late delivery affect customer satisfaction?

### Customer Experience
- What is the average review score?
- Which categories receive the best reviews?
- Does delivery performance affect review scores?
- Which sellers have the lowest customer satisfaction?

---

## 3. Dataset

### Source

**Brazilian E-Commerce Public Dataset by Olist**

### Files

```text
olist_customers_dataset.csv
olist_geolocation_dataset.csv
olist_order_items_dataset.csv
olist_order_payments_dataset.csv
olist_order_reviews_dataset.csv
olist_orders_dataset.csv
olist_products_dataset.csv
olist_sellers_dataset.csv
product_category_name_translation.csv
```

### Important Characteristics

- Approximately 100,000 orders
- 2016–2018 time period
- Relational structure
- Multiple items per order
- Multiple sellers
- Payments
- Reviews
- Customer and seller locations

The relational structure makes the dataset suitable for demonstrating real-world data modeling rather than simply analyzing a flat CSV.

---

## 4. Technology Stack

### Programming

```text
Python
Pandas
NumPy
Matplotlib
Seaborn
```

### Database

```text
PostgreSQL
```

### Analytics

```text
SQL
Jupyter Notebook
```

### Business Intelligence

```text
Power BI
DAX
Power Query
```

### Development

```text
VS Code
Git
GitHub
```

### Optional

```text
Docker
Great Expectations
Scikit-learn
```

---

## 5. Repository Structure

```text
sales-bi-dashboard/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_data_cleaning.ipynb
│   └── 03_eda.ipynb
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── data_loader.py
│   ├── data_cleaning.py
│   ├── feature_engineering.py
│   ├── database.py
│   └── pipeline.py
│
├── sql/
│   ├── 01_create_database.sql
│   ├── 02_create_raw_tables.sql
│   ├── 03_create_staging_tables.sql
│   ├── 04_create_analytics_model.sql
│   ├── 05_indexes.sql
│   ├── 06_data_quality.sql
│   ├── 07_business_metrics.sql
│   └── 08_analysis_queries.sql
│
├── powerbi/
│   └── sales_business_intelligence.pbix
│
├── docs/
│   ├── data_dictionary.md
│   ├── business_requirements.md
│   ├── data_model.md
│   └── business_insights.md
│
├── tests/
│   ├── test_cleaning.py
│   ├── test_transformations.py
│   └── test_data_quality.py
│
├── requirements.txt
├── .gitignore
├── docker-compose.yml
└── README.md
```

---

# 6. Phase 0 — Environment Setup

## Objective

Create a reproducible development environment.

### Install

```text
Python 3.x
PostgreSQL
pgAdmin
Power BI Desktop
Git
VS Code
```

### Python Dependencies

```text
pandas
numpy
sqlalchemy
psycopg2-binary
jupyter
matplotlib
seaborn
python-dotenv
openpyxl
```

Optional:

```text
scikit-learn
great-expectations
```

---

# 7. Phase 1 — Data Acquisition

## Objective

Download and preserve the original dataset.

Store all original files under:

```text
data/raw/
```

**Do not modify the raw files.**

Document:

- Dataset name
- Dataset URL
- Download date
- Source
- License
- Number of files
- Approximate number of records
- Time range

---

# 8. Phase 2 — Data Exploration

## Objective

Understand the data before writing transformations.

Create:

```text
notebooks/01_data_exploration.ipynb
```

For every table calculate:

- Number of rows
- Number of columns
- Data types
- Missing values
- Unique values
- Duplicate records
- Memory usage

Example:

```python
df.shape
df.info()
df.describe()
df.isna().sum()
df.nunique()
df.duplicated().sum()
```

---

# 9. Phase 3 — Data Dictionary

Create:

```text
docs/data_dictionary.md
```

For every column document:

- Column name
- Data type
- Description
- Primary key
- Foreign key
- Nullable
- Business meaning

Example:

```text
orders.order_id
----------------
Type: string
Role: Primary Key
Description: Unique identifier for an order
```

---

# 10. Phase 4 — Source Data Model

Core relationships:

```text
Customers
    │
    │ 1:N
    ▼
 Orders
    │
    ├───────────────┐
    │               │
    ▼               ▼
Order Items      Payments
    │
    ├──────────────┐
    │              │
    ▼              ▼
Products        Sellers

Orders
  │
  ▼
Reviews
```

Geolocation can enrich customer and seller locations.

---

# 11. Phase 5 — Data Cleaning

Create:

```text
notebooks/02_data_cleaning.ipynb
```

Production code:

```text
src/data_cleaning.py
```

## 11.1 Column Names

Standardize names:

```text
lowercase
snake_case
no spaces
```

Example:

```text
Order Purchase Timestamp
```

becomes:

```text
order_purchase_timestamp
```

---

## 11.2 Missing Values

Do not automatically delete missing values.

For each missing field determine:

- Why is it missing?
- Is missingness expected?
- Does missingness carry business meaning?
- Should it be removed?
- Should it be replaced?

Example:

A missing delivery date may mean that an order was never delivered.

Therefore:

```text
NULL ≠ automatically bad data
```

---

## 11.3 Date Processing

Convert timestamp fields to proper datetime types.

Important fields:

```text
order_purchase_timestamp
order_approved_at
order_delivered_carrier_date
order_delivered_customer_date
order_estimated_delivery_date
```

Create:

```text
purchase_date
purchase_year
purchase_quarter
purchase_month
purchase_month_name
purchase_week
purchase_day
purchase_day_of_week
```

---

# 12. Delivery Features

Create:

```text
delivery_days
estimated_delivery_days
delivery_delay_days
is_delivered
is_late
```

Definitions:

```text
delivery_days =
delivered_customer_date - purchase_timestamp
```

```text
delivery_delay_days =
delivered_customer_date - estimated_delivery_date
```

```text
is_late =
delivery_date > estimated_delivery_date
```

Handle non-delivered orders separately.

Do not treat missing delivery dates as zero.

---

# 13. Sales Features

Create:

```text
product_revenue = price
freight_value = freight_value
order_item_value = price + freight_value
```

## Important Financial Modeling Rule

The Olist dataset does **not** provide actual product acquisition cost.

Therefore:

> Do not calculate actual profit.

Use:

- Revenue
- Gross Merchandise Value
- Freight Value
- Average Order Value
- Average Item Price

If a hypothetical cost model is introduced later, label it explicitly as:

```text
Estimated Profit
```

and document every assumption.

---

# 14. Customer Features

The dataset contains:

```text
customer_id
customer_unique_id
```

These represent different concepts and should not be treated as identical.

Create:

```text
customer_order_count
customer_total_revenue
customer_average_order_value
customer_first_purchase_date
customer_last_purchase_date
is_repeat_customer
```

---

# 15. Product Features

Join:

```text
products
+
product_category_name_translation
```

Create:

```text
product_category_english
```

Keep the original Portuguese category as well.

---

# 16. Geographic Features

Use:

```text
customer_zip_code_prefix
seller_zip_code_prefix
```

Optionally enrich with:

```text
olist_geolocation_dataset.csv
```

Potential features:

```text
customer_latitude
customer_longitude
seller_latitude
seller_longitude
```

Optional advanced feature:

```text
seller_customer_distance_km
```

---

# 17. Payment Analysis

Payment data can contain multiple records for one order.

Therefore:

> Do not directly join payments to order items without considering grain.

Otherwise revenue can be duplicated.

Create an aggregation layer:

```text
order_id
total_payment_value
payment_count
primary_payment_type
max_installments
```

Analyze:

```text
Credit Card %
Pix %
Voucher %
Debit Card %
```

---

# 18. Review Analysis

Create:

```text
review_score
has_review
has_comment
```

Metrics:

```text
average_review_score
one_star_percentage
five_star_percentage
```

Optional:

```text
review_sentiment
```

---

# 19. Phase 6 — PostgreSQL Database

Create:

```text
olist_analytics
```

Schemas:

```text
raw
staging
analytics
```

Architecture:

```text
CSV
 ↓
raw
 ↓
staging
 ↓
analytics
 ↓
Power BI
```

---

# 20. Raw Layer

Create tables matching the original files:

```text
raw.customers
raw.orders
raw.order_items
raw.order_payments
raw.order_reviews
raw.products
raw.sellers
raw.geolocation
raw.category_translation
```

No business transformations should be performed in the raw layer.

---

# 21. Staging Layer

Create cleaned versions:

```text
staging.stg_customers
staging.stg_orders
staging.stg_order_items
staging.stg_payments
staging.stg_reviews
staging.stg_products
staging.stg_sellers
```

Tasks:

- Standardize data types
- Normalize names
- Handle invalid values
- Parse timestamps
- Add basic derived columns

---

# 22. Analytics Layer

Build a dimensional model.

Recommended:

```text
                    dim_customer
                         |
                         |
dim_product ---- fact_sales ---- dim_date
                         |
                         |
                    dim_seller
                         |
                         |
                    dim_location
```

Additional fact tables:

```text
fact_orders
fact_payments
fact_reviews
fact_delivery
```

This avoids forcing unrelated business processes into one enormous fact table.

---

# 23. Fact Tables

## fact_sales

**Grain:** One row per order item.

Fields:

```text
order_id
order_item_id
customer_key
product_key
seller_key
date_key
price
freight_value
item_value
```

## fact_orders

**Grain:** One row per order.

Fields:

```text
order_id
customer_key
purchase_date_key
order_status
approved_date
delivered_date
estimated_delivery_date
delivery_days
delay_days
is_late
```

## fact_payments

**Grain:** One payment transaction per order/payment record.

Fields:

```text
order_id
payment_type
payment_installments
payment_value
payment_sequence
```

## fact_reviews

**Grain:** One review record.

Fields:

```text
order_id
review_id
review_score
review_creation_date
review_answer_date
has_comment
```

---

# 24. Dimension Tables

## dim_customer

```text
customer_key
customer_unique_id
city
state
zip_prefix
```

## dim_product

```text
product_key
product_id
category_pt
category_en
weight
length
height
width
photos_qty
```

## dim_seller

```text
seller_key
seller_id
city
state
zip_prefix
```

## dim_date

```text
date_key
date
year
quarter
month
month_name
week
day
day_of_week
is_weekend
```

## dim_location

```text
location_key
zip_prefix
city
state
latitude
longitude
```

---

# 25. Database Integrity

Implement:

```text
PRIMARY KEY
FOREIGN KEY
UNIQUE
NOT NULL
CHECK
```

Examples:

```sql
CHECK (review_score BETWEEN 1 AND 5)
```

```sql
CHECK (price >= 0)
```

```sql
CHECK (freight_value >= 0)
```

Add indexes to frequently queried fields:

```text
order_id
customer_id
product_id
seller_id
order_purchase_timestamp
customer_state
product_category
```

---

# 26. Phase 8 — Data Quality

Create:

```text
sql/06_data_quality.sql
```

Tests should include:

## Uniqueness

- order_id
- product_id
- seller_id
- customer_id

## Referential Integrity

Check for:

- Orders without customers
- Order items without orders
- Order items without products
- Order items without sellers
- Payments without orders
- Reviews without orders

## Valid Ranges

```text
price >= 0
freight_value >= 0
review_score BETWEEN 1 AND 5
```

## Date Validation

Check:

```text
approval >= purchase
delivery >= purchase
estimated_delivery >= purchase
```

when applicable.

---

# 27. Phase 9 — SQL Business Analysis

Create:

```text
sql/08_analysis_queries.sql
```

Organize queries into:

- Sales
- Product
- Customer
- Geography
- Seller
- Operations
- Reviews

## Sales

- Monthly Revenue
- Monthly Orders
- Average Order Value
- Revenue Growth
- Orders Growth

## Product

- Top Products
- Top Categories
- Category Growth
- Average Product Price

## Customer

- Unique Customers
- Repeat Customers
- Customer Revenue
- Average Customer Revenue
- Top Customers

## Geography

- Revenue by State
- Orders by State
- AOV by State
- Delivery by State

## Seller

- Top Sellers
- Seller Revenue
- Seller Orders
- Seller Delivery Performance
- Seller Review Score

## Operations

- Average Delivery Time
- Late Delivery Rate
- Delivery by State
- Delivery by Seller

## Reviews

- Average Review Score
- Review Distribution
- Reviews by Category
- Reviews vs Delivery

---

# 28. Phase 10 — Business Metrics

## Total Revenue

```text
Total Revenue = SUM(price + freight_value)
```

Also report separately:

```text
Product Revenue
Freight Value
```

## Total Orders

```text
Total Orders = COUNT(DISTINCT order_id)
```

## Total Customers

```text
Total Customers = COUNT(DISTINCT customer_unique_id)
```

## Average Order Value

```text
AOV = Total Revenue / Total Orders
```

## Items per Order

```text
Items per Order = Total Items / Total Orders
```

## Repeat Customer Rate

```text
Repeat Customer Rate =
Customers with >1 order / Total Customers
```

## Average Delivery Days

```text
AVG(delivery_days)
```

for delivered orders only.

## Late Delivery Rate

```text
Late Delivery Rate =
Late Delivered Orders / Delivered Orders
```

## Average Review Score

```text
AVG(review_score)
```

---

# 29. Phase 11 — Time-Series Analysis

Analyze:

```text
Daily
Weekly
Monthly
Quarterly
Yearly
```

Metrics:

```text
Revenue
Orders
AOV
Review Score
Late Delivery Rate
MoM Growth
YoY Growth
```

Use YoY only where the historical period supports meaningful comparison.

---

# 30. Phase 12 — Customer Analytics

Implement RFM:

```text
R = Recency
F = Frequency
M = Monetary
```

Calculate:

### Recency

Days since customer's latest order.

### Frequency

Number of orders.

### Monetary

Total customer revenue.

Create:

```text
RFM Score
RFM Segment
```

Possible segments:

```text
Champions
Loyal Customers
Potential Loyalists
New Customers
At Risk
Lost Customers
```

Analyze:

```text
Revenue by Segment
Customers by Segment
AOV by Segment
```

---

# 31. Phase 13 — Product Analytics

Calculate:

```text
Revenue
Orders
Items Sold
Average Price
Average Review Score
```

For:

```text
Category
Product
```

Create drill-down:

```text
Category
   ↓
Product
   ↓
Revenue
Orders
Reviews
```

Identify:

- High-revenue categories
- Low-volume categories
- High-review categories
- Low-review categories
- High-demand products

---

# 32. Phase 14 — Customer Experience Analysis

Investigate:

```text
Delivery Time
      ↕
Late Delivery
      ↕
Review Score
```

Questions:

- Do late deliveries have lower reviews?
- Which states experience the most delays?
- Which sellers have high delay rates?
- Are specific categories more affected?

This connects:

```text
Operations
     ↓
Customer Experience
     ↓
Business Performance
```

---

# 33. Phase 15 — Power BI Data Model

Connect Power BI to the analytical PostgreSQL layer.

Do not build the dashboard directly from raw CSV files.

Recommended:

```text
PostgreSQL
     ↓
Power BI
```

Use a star-schema-oriented model.

---

# 34. Phase 16 — DAX

Create measures instead of hardcoding calculations in visuals.

Required measures:

```text
Total Revenue
Total Orders
Total Customers
Average Order Value
Average Review Score
Late Delivery %
Repeat Customer %
Revenue Growth %
```

Useful DAX functions:

```text
CALCULATE
DISTINCTCOUNT
SUM
AVERAGE
DIVIDE
DATE functions
```

Avoid unnecessary calculated columns when a measure is more appropriate.

---

# 35. Phase 17 — Power BI Dashboard

## Page 1 — Executive Overview

### KPI Cards

```text
Total Revenue
Total Orders
Total Customers
AOV
Average Review Score
Late Delivery %
```

### Charts

```text
Revenue Trend
Orders Trend
Revenue by Category
Revenue by State
```

### Filters

```text
Date
State
Category
Order Status
```

Purpose:

> Give management an immediate understanding of business performance.

---

## Page 2 — Sales & Product Performance

Visuals:

```text
Top 10 Products
Revenue by Category
Orders by Category
Revenue Trend by Category
Average Order Value
```

Add:

```text
Category → Product
```

drill-down.

Purpose:

> Identify what products and categories drive the business.

---

## Page 3 — Customer Analytics

Visuals:

```text
New vs Returning Customers
Revenue by RFM Segment
Customer Distribution
Top Customers
Revenue per Customer
```

Include RFM segmentation.

Purpose:

> Understand customer value and retention behavior.

---

## Page 4 — Operations & Customer Satisfaction

Visuals:

```text
Average Delivery Days
Late Delivery %
Delivery Performance by State
Review Score Distribution
Review Score vs Delivery Performance
Seller Performance
```

Purpose:

> Identify operational problems that affect customer satisfaction.

---

# 36. Phase 18 — Dashboard UX

Implement slicers:

```text
Date
State
City
Category
Seller
Order Status
Payment Type
```

Implement:

- Drill-through
- Tooltips
- Navigation
- Consistent KPI cards
- Clear titles
- Business-oriented visual hierarchy

Possible navigation:

```text
Overview
Sales
Customers
Operations
```

---

# 37. Phase 19 — Business Insights

Do not write insights before completing the analysis.

Every important finding should follow:

```text
Observation
    ↓
Evidence
    ↓
Business Impact
    ↓
Recommendation
```

Example:

```text
Observation:
Late deliveries have lower average review scores.

Evidence:
Compare review scores for late vs on-time orders.

Impact:
Delivery performance may negatively affect customer satisfaction.

Recommendation:
Prioritize logistics improvements in high-delay regions.
```

The actual numerical findings must come from the dataset.

---

# 38. Phase 20 — Advanced Analysis

These are optional but highly recommended after the core project.

## Sales Forecasting

```text
Historical Monthly Revenue
        ↓
Time Series Model
        ↓
Future Forecast
```

Possible models:

```text
Moving Average
Exponential Smoothing
ARIMA
Prophet
```

Forecasting should remain an extension rather than the main purpose.

## Sentiment Analysis

Analyze:

```text
review_comment_message
```

Classify:

```text
Positive
Neutral
Negative
```

Compare sentiment with:

```text
Delivery Time
Product Category
Seller
Review Score
```

## Geospatial Analysis

Use:

```text
Latitude
Longitude
```

Analyze:

```text
Customer Density
Seller Density
Regional Revenue
Delivery Distance
```

Optional:

```text
Seller → Customer Distance
```

---

# 39. Phase 21 — Testing

## Unit Tests

Test Python functions:

```text
test_clean_dates()
test_clean_prices()
test_customer_features()
test_delivery_features()
```

## Data Tests

```text
test_no_negative_prices()
test_valid_review_scores()
test_unique_orders()
test_valid_foreign_keys()
```

## SQL Tests

Validate:

```text
row counts
NULL rates
orphan records
duplicate keys
```

---

# 40. Phase 22 — Reproducibility

A recruiter should be able to clone the repository and understand how to reproduce the project.

Document:

1. Download dataset
2. Install dependencies
3. Configure PostgreSQL
4. Load raw data
5. Run transformations
6. Run quality checks
7. Connect Power BI

Avoid undocumented manual transformations.

---

# 41. Phase 23 — Docker

Optional advanced implementation.

Create:

```text
docker-compose.yml
```

Services:

```text
postgres
pgadmin
```

Architecture:

```text
Docker
 ├── PostgreSQL
 └── pgAdmin
```

The goal is to make database setup reproducible.

---

# 42. Phase 24 — Git & GitHub

Use meaningful commits:

```text
initial project setup
add raw data ingestion
implement data cleaning
add PostgreSQL schema
add data quality checks
implement business metrics
add RFM analysis
build Power BI dashboard
add business insights
update README
```

Do not commit:

```text
.env
passwords
database credentials
large raw datasets
```

Use `.gitignore`.

---

# 43. Phase 25 — README

The README should contain:

```text
# Sales & Business Intelligence Dashboard

## Overview

## Business Problem

## Dataset

## Architecture

## Tech Stack

## Data Model

## Data Cleaning

## SQL Analysis

## Business Metrics

## Dashboard

## Key Insights

## Recommendations

## Project Structure

## Installation

## Usage

## Future Improvements
```

Include:

- Dashboard screenshots
- Architecture diagram
- ERD
- Example insights

---

# 44. Final Deliverables

The final repository should contain:

- Python pipeline
- SQL scripts
- PostgreSQL schema
- Data dictionary
- Data quality tests
- EDA notebook
- Power BI dashboard
- Business insights
- Architecture diagram
- ERD
- README
- Optional Docker environment

---

# 45. Definition of Done

- [ ] Dataset downloaded and documented
- [ ] Raw data preserved
- [ ] Data exploration completed
- [ ] Data dictionary created
- [ ] Missing values analyzed
- [ ] Duplicates analyzed
- [ ] Data types standardized
- [ ] Dates processed
- [ ] Delivery features created
- [ ] Customer features created
- [ ] Product features created
- [ ] Payment grain handled correctly
- [ ] Review grain handled correctly
- [ ] PostgreSQL database created
- [ ] Raw schema created
- [ ] Staging schema created
- [ ] Analytics schema created
- [ ] Primary/foreign keys implemented
- [ ] Indexes created
- [ ] Data quality tests implemented
- [ ] Business metrics implemented
- [ ] SQL analysis completed
- [ ] RFM analysis completed
- [ ] Power BI model created
- [ ] DAX measures created
- [ ] Executive dashboard completed
- [ ] Sales dashboard completed
- [ ] Customer dashboard completed
- [ ] Operations dashboard completed
- [ ] Filters implemented
- [ ] Drill-through implemented
- [ ] Tooltips implemented
- [ ] Business insights documented
- [ ] Recommendations documented
- [ ] Automated tests added
- [ ] GitHub repository organized
- [ ] README completed
- [ ] Screenshots added
- [ ] Optional Docker environment completed

---

# 46. Final Architecture

```text
                    ┌─────────────────────┐
                    │   Olist CSV Files   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │       Python        │
                    │  Pandas / NumPy     │
                    └──────────┬──────────┘
                               │
                        Data Cleaning
                               │
                               ▼
                    ┌─────────────────────┐
                    │     PostgreSQL      │
                    │                     │
                    │  ┌───────────────┐  │
                    │  │     Raw       │  │
                    │  ├───────────────┤  │
                    │  │   Staging     │  │
                    │  ├───────────────┤  │
                    │  │   Analytics   │  │
                    │  └───────────────┘  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │        SQL          │
                    │ Business Analytics  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │      Power BI       │
                    │                     │
                    │ Executive Overview  │
                    │ Sales & Products    │
                    │ Customers           │
                    │ Operations          │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Business Insights   │
                    │ & Recommendations   │
                    └─────────────────────┘
```

---

# 47. Skill Coverage

| Skill | Demonstrated Through |
|---|---|
| Python | Cleaning, transformation, automation |
| Pandas | Data manipulation |
| SQL | Analytics and transformations |
| PostgreSQL | Database implementation |
| Data Modeling | Fact/dimension design |
| Data Cleaning | Missing values, duplicates, types |
| Data Quality | Validation and tests |
| Power BI | Dashboard |
| DAX | Business metrics |
| Statistics | RFM, trends, distributions |
| Business Analysis | Insights and recommendations |
| Git/GitHub | Version control |
| Docker | Reproducible environment |
| Data Visualization | Power BI |
| ETL | Raw → Staging → Analytics |

---

# 48. Portfolio Positioning

Use the project title:

> **End-to-End E-Commerce Sales & Business Intelligence Analytics Platform**

Avoid presenting it merely as:

> Olist Dataset Analysis

The project should communicate the complete workflow:

```text
Business Problem
      ↓
Data Acquisition
      ↓
Data Understanding
      ↓
Data Cleaning
      ↓
Data Modeling
      ↓
SQL
      ↓
Business Metrics
      ↓
Visualization
      ↓
Insights
      ↓
Recommendations
```

---

# 49. Success Criteria

A recruiter should be able to conclude that the candidate can:

1. Understand a messy real-world dataset.
2. Identify business questions.
3. Clean and validate data.
4. Design a relational analytical model.
5. Write non-trivial SQL.
6. Create meaningful KPIs.
7. Build an interactive BI dashboard.
8. Explain findings in business language.
9. Make evidence-based recommendations.
10. Produce reproducible and maintainable analytics work.

The goal is not simply to demonstrate Power BI.

The goal is to demonstrate the ability to take:

> **Raw Business Data → Business Decision**

---

# 50. Recommended Implementation Order

```text
Phase 0  → Environment Setup
Phase 1  → Dataset Acquisition
Phase 2  → Data Exploration
Phase 3  → Data Dictionary
Phase 4  → Source Data Model
Phase 5  → Data Cleaning
Phase 6  → PostgreSQL
Phase 7  → Data Modeling
Phase 8  → Data Quality
Phase 9  → SQL Analysis
Phase 10 → Business Metrics
Phase 11 → Time-Series Analysis
Phase 12 → Customer/RFM Analysis
Phase 13 → Product Analysis
Phase 14 → Customer Experience
Phase 15 → Power BI Model
Phase 16 → DAX
Phase 17 → Dashboard
Phase 18 → Dashboard UX
Phase 19 → Business Insights
Phase 20 → Advanced Analysis
Phase 21 → Testing
Phase 22 → Reproducibility
Phase 23 → Docker
Phase 24 → GitHub
Phase 25 → README
```

## Final Deliverable

A professional, reproducible E-Commerce Business Intelligence Platform combining:

```text
Python
+
PostgreSQL
+
SQL
+
Power BI
+
Business Analysis
+
Data Quality
+
Optional Advanced Analytics
```

The end result should demonstrate the full path from:

**Raw Data → Clean Data → Analytical Model → KPIs → Dashboard → Business Insights → Recommendations.**
