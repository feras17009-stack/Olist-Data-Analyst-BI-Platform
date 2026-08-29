# Business Requirements Document (BRD)
## End-to-End E-Commerce Analytics Platform

---

## 1. Executive Summary

This project delivers an enterprise-grade Business Intelligence and Analytics platform for an e-commerce marketplace operating across Brazil. The platform empowers leadership, commercial teams, category managers, and logistics operations with reliable, single-source-of-truth data to evaluate growth, customer loyalty, logistics bottlenecks, and vendor quality.

---

## 2. Stakeholder Objectives & Key Questions

### 2.1 C-Suite / Executive Leadership
- **Total Revenue & Volume:** What is our historical revenue run rate and how is it growing quarter-over-quarter?
- **Basket Quality:** What is the platform Average Order Value (AOV) and items per order?
- **Customer Acquisition vs Retention:** What percentage of our revenue comes from repeat buyers vs new customer acquisition?
- **Delivery Satisfaction:** How does our operational fulfillment performance correlate with customer satisfaction (NPS / CSAT)?

### 2.2 Commercial & Category Management
- **Category Leadership:** Which categories are top revenue generators vs high-volume margin contributors?
- **Catalog Optimization:** What is the average item price across product categories?
- **Underperforming Segments:** Which categories experience high cancellation or below-average review scores?

### 2.3 Marketing & Customer Success
- **Customer Lifetime Value (CLV):** Who are our highest-value customers and what segments do they occupy?
- **RFM Segmentation:** How many customers are "Champions" vs "At Risk" or "Lost"?
- **Regional Demand:** Which states and metropolitan regions have the highest density of orders?

### 2.4 Logistics & Operations
- **Fulfillment Turnaround:** What is the average delivery turnaround from order placement to doorstep?
- **SLA Breach Rate:** What percentage of orders are delivered past the promised estimated delivery date?
- **Regional Delivery Bottlenecks:** Which states experience disproportionate logistics delays?
- **Merchant Compliance:** Which sellers consistently deliver orders late or receive low customer review ratings?

---

## 3. Business Metric Definitions & Mathematical Formulas

| Metric Name | Calculation / Formula | Business Grain | Target SLA / Benchmark |
|---|---|---|---|
| **Gross Merchandise Value (GMV)** | $\sum (\text{item price} + \text{freight value})$ | Line Item / Order / Time | Growth > 15% QoQ |
| **Product Revenue** | $\sum (\text{item price})$ | Line Item | Core merchandising revenue |
| **Freight Revenue** | $\sum (\text{freight value})$ | Line Item | Shipping cost recovery |
| **Total Orders** | $\text{COUNT}(\text{DISTINCT } \text{order\_id})$ | Order Grain | Order volume tracking |
| **Average Order Value (AOV)** | $\frac{\text{Total Revenue}}{\text{Total Orders}}$ | Platform / Segment / State | Target > R\$ 150.00 |
| **Items Per Order** | $\frac{\text{Total Items Sold}}{\text{Total Orders}}$ | Platform / Category | Target > 1.15 items |
| **Repeat Customer Rate** | $\frac{\text{Customers with } > 1 \text{ Lifetime Orders}}{\text{Total Unique Customers}} \times 100$ | Customer Grain | Monitor customer retention |
| **Average Delivery Days** | $\text{AVG}(\text{delivered\_timestamp} - \text{purchase\_timestamp})$ | Delivered Orders | Target < 12.0 Days |
| **Late Delivery Rate (%)** | $\frac{\text{Delivered Orders where Actual Delivery } > \text{ Estimated Delivery}}{\text{Total Delivered Orders}} \times 100$ | Delivered Orders | Target < 5.0% |
| **Average Review Score (CSAT)** | $\text{AVG}(\text{review\_score})$ | Order Reviews (1 to 5) | Target > 4.2 / 5.0 |

---

## 4. Key Constraints & Data Integrity Principles

1. **Financial Rule on Profitability:** The Olist dataset provides product selling prices and freight charged, but **does not** supply merchant acquisition costs (COGS). The platform explicitly measures **Revenue, GMV, and AOV** without fabricating non-existent cost structures.
2. **Grain Separation:** Payment transactions and Order Items operate at different cardinalities (one order can have 3 items and 2 payment split-tenders). To prevent Cartesian duplication of revenue, financial metrics must be calculated strictly from `fact_sales` and `fact_orders`.
3. **Delivery Date Handling:** Cancelled and in-transit orders have null delivery timestamps. Calculations for `delivery_days` and `is_late` must strictly filter on `order_status = 'delivered'` and non-null timestamps to avoid skewing averages with zeros.
