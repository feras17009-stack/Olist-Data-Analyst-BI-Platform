# Power BI Dashboard Design & Architecture Specification

## 1. Dashboard Layout & Navigation Structure

```text
┌────────────────────────────────────────────────────────────────────────┐
│  OLIST BRAZILIAN E-COMMERCE BUSINESS INTELLIGENCE PLATFORM             │
├──────────────┬───────────────────┬───────────────────┬─────────────────┤
│ [1] Overview │ [2] Sales/Product │ [3] Customer/RFM  │ [4] Operations  │
└──────────────┴───────────────────┴───────────────────┴─────────────────┘
```

---

## 2. Page Specifications

### Page 1: Executive Overview
**Target Audience:** CEO, COO, CFO, VP of Marketplace  
**Primary Goal:** Real-time visibility into top-line revenue, order volumes, customer acquisition, fulfillment health, and customer satisfaction.

1. **Top KPI Ribbon (6 Cards):**
   - **Total Gross Revenue:** `R$ 15.84M` (Subtext: Product: `R$ 13.59M` | Freight: `R$ 2.25M`)
   - **Total Orders:** `99,441` (Delivered: `96,478`)
   - **Unique Customers:** `96,096` (Repeat Rate: `2.99%`)
   - **Average Order Value (AOV):** `R$ 159.33` (Target: `R$ 150.00`)
   - **Late Delivery SLA Breach %:** `8.11%` (Target: `< 5.0%` [Conditional Alert: Amber/Red])
   - **Average Review CSAT:** `4.09 / 5.0` (Target: `4.20 / 5.0`)

2. **Visuals:**
   - **Monthly Revenue & Order Volume Growth:** Dual-axis Area & Line Chart (`year_month` vs `[Total Revenue]` & `[Total Orders]`).
   - **Top 5 Revenue Generating Categories:** Horizontal Bar Chart (`product_category_name_english` vs `[Total Revenue]`).
   - **Geographic Revenue Heatmap (Brazil States):** Map/Shape visual with color saturation based on `[Total Revenue]`.
   - **Order Fulfillment Status:** Donut chart (`order_status` distribution: `delivered`, `shipped`, `canceled`, `invoiced`).

3. **Interactive Slicers:**
   - Date Range (`dim_date[full_date]`)
   - State Slicer (`dim_customer[customer_state]`)
   - Category Slicer (`dim_product[product_category_name_english]`)

---

### Page 2: Sales & Product Performance
**Target Audience:** Chief Commercial Officer, Category Managers, Merchandising Leads  
**Primary Goal:** Identify high-margin categories, growth trends, SKU performance, and basket economics.

1. **KPI Cards:**
   - Total Units Sold (`112,650`)
   - Average Item Price (`R$ 120.65`)
   - Items per Order (`1.13`)
   - Product Revenue (`R$ 13.59M`)

2. **Visuals:**
   - **Category Revenue vs Volume Matrix (Scatter / Bubble Plot):** X-axis: `Total Units Sold`, Y-axis: `Total Revenue`, Bubble Size: `AOV`.
   - **Top 10 Selling Products:** Bar chart with drill-down hierarchy (`Category -> Product ID`).
   - **Category Monthly Revenue Trajectory:** 100% Stacked Area Chart showing category mix evolution.
   - **Freight Cost Ratio by Category:** Column chart displaying `[Freight Share %]`.

---

### Page 3: Customer Analytics & RFM Segmentation
**Target Audience:** VP of Marketing, CRM Lead, Retention Managers  
**Primary Goal:** Understand customer lifetime spend, churn risks, and loyalty segmentation.

1. **KPI Cards:**
   - Total Customers (`96,096`)
   - Repeat Buyers (`2,997`)
   - Potential Loyalists Spend (`R$ 6.03M` / 38.1%)
   - At Risk & Lost Spend (`R$ 4.07M` / 25.7%)

2. **Visuals:**
   - **RFM Segment Treemap:** Sized by `[Total Revenue]` and labeled with customer counts.
   - **Customer Lifetime Value Distribution:** Histogram / Binned bar chart of `rfm_monetary`.
   - **Repeat Purchase Behavior:** Stacked bar chart comparing Single vs Multi-purchase spend.
   - **Top Customer Spend Leaderboard:** Matrix table (`customer_unique_id`, `state`, `RFM Segment`, `Lifetime Orders`, `Total Spend`).

---

### Page 4: Operations, Logistics & Customer Experience
**Target Audience:** Head of Supply Chain, Logistics Operations, Customer Support VP  
**Primary Goal:** Isolate delivery bottlenecks, investigate delivery delay impact on CSAT, and evaluate merchant fulfillment performance.

1. **KPI Cards:**
   - Average Delivery Days (`12.6 Days`)
   - Average Estimated Delivery Days (`24.2 Days`)
   - Delayed Orders (`7,661`)
   - Review Score on Delayed Orders (`2.57 / 5.0`) vs On-Time (`4.29 / 5.0`)

2. **Visuals:**
   - **Delivery Performance vs Customer Satisfaction Correlation:** Grouped column chart comparing CSAT and % 1-star reviews for On-Time vs Delayed orders.
   - **State-Level Delivery Days & Late Rate:** Clustered bar chart showing `Average Delivery Days` and `Late Delivery %` by `customer_state`.
   - **Seller Fulfillment Compliance Matrix:** Scatter plot of `Total Orders Fulfilled` vs `Seller Late %`.
   - **Review Score Breakdown:** 100% Stacked horizontal bar chart showing distribution of 1 to 5 star ratings.
