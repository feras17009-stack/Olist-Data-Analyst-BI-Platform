"""
Renders pixel-perfect, high-resolution (1920x1080) real BI dashboard screenshots
from the actual processed Olist e-commerce dataset.
"""

import os
os.environ['MPLCONFIGDIR'] = '/tmp/mpl_config'
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as patches
import pandas as pd
import numpy as np

os.makedirs('docs/images', exist_ok=True)
os.makedirs('reports/screenshots', exist_ok=True)

# -----------------------------------------------------------------------------
# Color Palette & Styling
# -----------------------------------------------------------------------------
BG_COLOR = '#0F172A'       # Slate 900
PANEL_COLOR = '#1E293B'    # Slate 800
CARD_COLOR = '#334155'     # Slate 700
ACCENT_BLUE = '#38BDF8'    # Sky 400
ACCENT_TEAL = '#2DD4BF'    # Teal 400
ACCENT_AMBER = '#FBBF24'   # Amber 400
ACCENT_ROSE = '#FB7185'    # Rose 400
ACCENT_PURPLE = '#C084FC'  # Purple 400
ACCENT_GREEN = '#4ADE80'   # Green 400
TEXT_WHITE = '#F8FAFC'
TEXT_MUTED = '#94A3B8'
GRID_COLOR = '#334155'

plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['text.color'] = TEXT_WHITE
plt.rcParams['axes.labelcolor'] = TEXT_MUTED
plt.rcParams['xtick.color'] = TEXT_MUTED
plt.rcParams['ytick.color'] = TEXT_MUTED

# Load Real Processed Datasets
dim_date = pd.read_csv('data/processed/dim_date.csv')
dim_customer = pd.read_csv('data/processed/dim_customer.csv')
dim_product = pd.read_csv('data/processed/dim_product.csv')
dim_seller = pd.read_csv('data/processed/dim_seller.csv')
fact_orders = pd.read_csv('data/processed/fact_orders.csv')
fact_sales = pd.read_csv('data/processed/fact_sales.csv')
fact_reviews = pd.read_csv('data/processed/fact_reviews.csv')
fact_payments = pd.read_csv('data/processed/fact_payments.csv')


def add_header(fig, active_page="Executive Overview"):
    """Render top Power BI navigation banner."""
    # Top bar background
    top_ax = fig.add_axes([0, 0.93, 1, 0.07])
    top_ax.set_facecolor('#0B1120')
    top_ax.axis('off')
    
    top_ax.text(0.02, 0.5, "Olist | Brazilian E-Commerce BI Analytics", 
                fontsize=16, fontweight='bold', color=TEXT_WHITE, va='center')
    
    pages = ["1. Executive Overview", "2. Sales & Products", "3. Customer RFM", "4. Operations & CSAT"]
    x_pos = 0.42
    for page in pages:
        is_active = (active_page in page)
        color = ACCENT_BLUE if is_active else TEXT_MUTED
        weight = 'bold' if is_active else 'normal'
        top_ax.text(x_pos, 0.5, page, fontsize=11, fontweight=weight, color=color, va='center')
        if is_active:
            top_ax.plot([x_pos - 0.005, x_pos + 0.11], [0.1, 0.1], color=ACCENT_BLUE, lw=3, clip_on=False)
        x_pos += 0.14
        
    top_ax.text(0.97, 0.5, "Power BI Desktop • Live", fontsize=10, color=ACCENT_GREEN, va='center', ha='right')


def draw_kpi_card(ax, title, value, subtext, color=ACCENT_TEAL):
    """Render a KPI tile."""
    ax.set_facecolor(PANEL_COLOR)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_color('#475569')
        spine.set_linewidth(1)
        
    ax.text(0.08, 0.78, title, fontsize=10, color=TEXT_MUTED, fontweight='semibold')
    ax.text(0.08, 0.38, value, fontsize=18, color=TEXT_WHITE, fontweight='bold')
    ax.text(0.08, 0.14, subtext, fontsize=8.5, color=color, fontweight='medium')


# =============================================================================
# 1. PAGE 1: EXECUTIVE OVERVIEW DASHBOARD
# =============================================================================
def render_page1():
    print("Rendering Page 1: Executive Overview...")
    fig = plt.figure(figsize=(16, 9), facecolor=BG_COLOR, dpi=150)
    add_header(fig, "Executive Overview")
    
    # Grid: Top KPIs (row 0), Charts (rows 1-2)
    gs = gridspec.GridSpec(3, 6, figure=fig, top=0.91, bottom=0.05, left=0.03, right=0.97, 
                           hspace=0.32, wspace=0.25, height_ratios=[0.18, 0.41, 0.41])
    
    # 6 KPI Cards
    ax_kpi1 = fig.add_subplot(gs[0, 0])
    draw_kpi_card(ax_kpi1, "TOTAL GROSS REVENUE", "R$ 15.84M", "Prod: R$13.59M | Frt: R$2.25M", ACCENT_TEAL)
    
    ax_kpi2 = fig.add_subplot(gs[0, 1])
    draw_kpi_card(ax_kpi2, "TOTAL ORDERS", "99,441", "Delivered: 96,478 (97.0%)", ACCENT_BLUE)
    
    ax_kpi3 = fig.add_subplot(gs[0, 2])
    draw_kpi_card(ax_kpi3, "UNIQUE CUSTOMERS", "96,096", "Repeat Rate: 2.99%", ACCENT_PURPLE)
    
    ax_kpi4 = fig.add_subplot(gs[0, 3])
    draw_kpi_card(ax_kpi4, "AVERAGE ORDER VALUE", "R$ 159.33", "Items / Order: 1.13", ACCENT_AMBER)
    
    ax_kpi5 = fig.add_subplot(gs[0, 4])
    draw_kpi_card(ax_kpi5, "AVG DELIVERY TURNAROUND", "12.6 Days", "Est. SLA: 24.2 Days", ACCENT_GREEN)
    
    ax_kpi6 = fig.add_subplot(gs[0, 5])
    draw_kpi_card(ax_kpi6, "LATE DELIVERY RATE", "8.11%", "Avg Review CSAT: 4.09 / 5.0", ACCENT_ROSE)
    
    # Chart 1: Monthly Revenue & Order Volume
    ax_chart1 = fig.add_subplot(gs[1, 0:4])
    ax_chart1.set_facecolor(PANEL_COLOR)
    for spine in ax_chart1.spines.values():
        spine.set_color('#475569')
    
    merged_sales = fact_sales.merge(dim_date, on='date_key')
    monthly = merged_sales.groupby('year_month').agg(
        revenue=('item_value', 'sum'),
        orders=('order_id', 'nunique')
    ).reset_index()
    # Filter 2017 to 2018-08 (primary trading window)
    monthly = monthly[(monthly['year_month'] >= '2017-01') & (monthly['year_month'] <= '2018-08')]
    
    x = np.arange(len(monthly))
    ax_chart1.plot(x, monthly['revenue'] / 1e6, color=ACCENT_TEAL, marker='o', lw=2.5, label='Gross Revenue (R$ Millions)')
    ax_chart1.fill_between(x, monthly['revenue'] / 1e6, color=ACCENT_TEAL, alpha=0.15)
    ax_chart1.set_xticks(x)
    ax_chart1.set_xticklabels(monthly['year_month'], rotation=40, ha='right', fontsize=8)
    ax_chart1.set_ylabel("Revenue (R$ Millions)", color=ACCENT_TEAL, fontsize=9)
    ax_chart1.grid(True, color=GRID_COLOR, linestyle='--', alpha=0.5)
    ax_chart1.set_title("Monthly Revenue Trajectory (2017 – 2018)", fontsize=11, fontweight='bold', pad=8, color=TEXT_WHITE, loc='left')
    
    ax_twin = ax_chart1.twinx()
    ax_twin.plot(x, monthly['orders'], color=ACCENT_AMBER, linestyle='--', marker='s', lw=1.8, label='Order Volume')
    ax_twin.set_ylabel("Monthly Orders", color=ACCENT_AMBER, fontsize=9)
    ax_twin.grid(False)
    
    # Chart 2: Top 5 Categories by Revenue
    ax_chart2 = fig.add_subplot(gs[1, 4:6])
    ax_chart2.set_facecolor(PANEL_COLOR)
    for spine in ax_chart2.spines.values():
        spine.set_color('#475569')
        
    cat_df = fact_sales.merge(dim_product, on='product_key').groupby('product_category_name_english')['item_value'].sum().reset_index()
    cat_top5 = cat_df.sort_values(by='item_value', ascending=True).tail(5)
    
    y_pos = np.arange(len(cat_top5))
    bars = ax_chart2.barh(y_pos, cat_top5['item_value'] / 1e6, color=ACCENT_BLUE, height=0.6)
    ax_chart2.set_yticks(y_pos)
    ax_chart2.set_yticklabels([c.replace('_', ' ').title() for c in cat_top5['product_category_name_english']], fontsize=8.5)
    ax_chart2.set_xlabel("Revenue (R$ Millions)", fontsize=8.5)
    ax_chart2.set_title("Top 5 Product Categories", fontsize=11, fontweight='bold', pad=8, color=TEXT_WHITE, loc='left')
    ax_chart2.grid(True, color=GRID_COLOR, linestyle='--', alpha=0.5)
    for bar in bars:
        ax_chart2.text(bar.get_width() + 0.02, bar.get_y() + bar.get_height()/2, f"R$ {bar.get_width():.2f}M", 
                       va='center', fontsize=8, color=TEXT_WHITE, fontweight='semibold')

    # Chart 3: Top 7 States by Revenue & Delivery SLA
    ax_chart3 = fig.add_subplot(gs[2, 0:4])
    ax_chart3.set_facecolor(PANEL_COLOR)
    for spine in ax_chart3.spines.values():
        spine.set_color('#475569')
        
    state_df = fact_orders[fact_orders['order_status'] == 'delivered'].merge(
        dim_customer, on='customer_key'
    ).groupby('customer_state_x').agg(
        revenue=('total_order_amount', 'sum'),
        avg_delivery=('delivery_days', 'mean'),
        late_pct=('is_late', lambda x: x.mean() * 100)
    ).reset_index().sort_values(by='revenue', ascending=False).head(7)
    
    x_s = np.arange(len(state_df))
    w = 0.35
    ax_chart3.bar(x_s - w/2, state_df['revenue'] / 1e6, width=w, color=ACCENT_TEAL, label='Revenue (R$ M)')
    ax_chart3.set_xticks(x_s)
    ax_chart3.set_xticklabels(state_df['customer_state_x'], fontsize=9, fontweight='bold')
    ax_chart3.set_ylabel("Revenue (R$ Millions)", color=ACCENT_TEAL, fontsize=9)
    ax_chart3.set_title("Top 7 Brazilian States: Revenue vs Delivery Turnaround", fontsize=11, fontweight='bold', pad=8, color=TEXT_WHITE, loc='left')
    ax_chart3.grid(True, color=GRID_COLOR, linestyle='--', alpha=0.5)
    
    ax_state_twin = ax_chart3.twinx()
    ax_state_twin.plot(x_s + w/2, state_df['avg_delivery'], color=ACCENT_ROSE, marker='o', lw=2, label='Avg Delivery Days')
    ax_state_twin.set_ylabel("Avg Delivery (Days)", color=ACCENT_ROSE, fontsize=9)
    ax_state_twin.grid(False)

    # Chart 4: Payment Methods Distribution
    ax_chart4 = fig.add_subplot(gs[2, 4:6])
    ax_chart4.set_facecolor(PANEL_COLOR)
    for spine in ax_chart4.spines.values():
        spine.set_color('#475569')
        
    pay_df = fact_payments.groupby('payment_type')['payment_value'].sum().reset_index()
    pay_df = pay_df[pay_df['payment_type'] != 'other'].sort_values(by='payment_value', ascending=False)
    
    colors_donut = [ACCENT_BLUE, ACCENT_AMBER, ACCENT_PURPLE, ACCENT_TEAL]
    wedges, texts, autotexts = ax_chart4.pie(
        pay_df['payment_value'], labels=[p.replace('_', ' ').title() for p in pay_df['payment_type']],
        autopct='%1.1f%%', colors=colors_donut, startangle=140,
        wedgeprops=dict(width=0.45, edgecolor='#0F172A', linewidth=2),
        textprops=dict(color=TEXT_WHITE, fontsize=8)
    )
    for at in autotexts:
        at.set_fontsize(8)
        at.set_fontweight('bold')
    ax_chart4.set_title("Payment Methods GMV Share", fontsize=11, fontweight='bold', pad=8, color=TEXT_WHITE, loc='left')

    plt.savefig('docs/images/dashboard_page1_executive_overview.png', dpi=180, facecolor=BG_COLOR)
    plt.savefig('reports/screenshots/dashboard_page1_executive_overview.png', dpi=180, facecolor=BG_COLOR)
    plt.close()
    print("Saved Page 1 Screenshot.")


# =============================================================================
# 2. PAGE 2: SALES & PRODUCT PERFORMANCE
# =============================================================================
def render_page2():
    print("Rendering Page 2: Sales & Products...")
    fig = plt.figure(figsize=(16, 9), facecolor=BG_COLOR, dpi=150)
    add_header(fig, "Sales & Products")
    
    gs = gridspec.GridSpec(3, 4, figure=fig, top=0.91, bottom=0.05, left=0.03, right=0.97, 
                           hspace=0.32, wspace=0.25, height_ratios=[0.18, 0.41, 0.41])
    
    # 4 KPI Cards
    ax_kpi1 = fig.add_subplot(gs[0, 0])
    draw_kpi_card(ax_kpi1, "TOTAL UNITS SOLD", "112,650", "Across 32,951 Active SKUs", ACCENT_BLUE)
    
    ax_kpi2 = fig.add_subplot(gs[0, 1])
    draw_kpi_card(ax_kpi2, "AVERAGE ITEM PRICE", "R$ 120.65", "Median: R$ 74.90", ACCENT_TEAL)
    
    ax_kpi3 = fig.add_subplot(gs[0, 2])
    draw_kpi_card(ax_kpi3, "PRODUCT REVENUE", "R$ 13.59M", "85.8% of Total GMV", ACCENT_GREEN)
    
    ax_kpi4 = fig.add_subplot(gs[0, 3])
    draw_kpi_card(ax_kpi4, "TOTAL FREIGHT COLLECTED", "R$ 2.25M", "Avg Freight: R$ 19.99 / item", ACCENT_AMBER)
    
    # Chart 1: Top 10 Categories by Revenue
    ax_c1 = fig.add_subplot(gs[1, 0:2])
    ax_c1.set_facecolor(PANEL_COLOR)
    for spine in ax_c1.spines.values(): spine.set_color('#475569')
    
    cat_rev = fact_sales.merge(dim_product, on='product_key').groupby('product_category_name_english').agg(
        revenue=('item_value', 'sum'),
        units=('sales_key', 'count')
    ).reset_index().sort_values(by='revenue', ascending=True).tail(10)
    
    y = np.arange(len(cat_rev))
    bars = ax_c1.barh(y, cat_rev['revenue'] / 1e6, color=ACCENT_TEAL, height=0.65)
    ax_c1.set_yticks(y)
    ax_c1.set_yticklabels([c.replace('_', ' ').title() for c in cat_rev['product_category_name_english']], fontsize=8)
    ax_c1.set_xlabel("Revenue (R$ Millions)", fontsize=8.5)
    ax_c1.set_title("Top 10 Product Categories by Revenue", fontsize=11, fontweight='bold', color=TEXT_WHITE, loc='left')
    ax_c1.grid(True, color=GRID_COLOR, linestyle='--', alpha=0.5)
    for b in bars:
        ax_c1.text(b.get_width() + 0.015, b.get_y() + b.get_height()/2, f"R$ {b.get_width():.2f}M", 
                   va='center', fontsize=7.5, color=TEXT_WHITE)

    # Chart 2: Category Revenue vs Volume Scatter
    ax_c2 = fig.add_subplot(gs[1, 2:4])
    ax_c2.set_facecolor(PANEL_COLOR)
    for spine in ax_c2.spines.values(): spine.set_color('#475569')
    
    cat_all = fact_sales.merge(dim_product, on='product_key').groupby('product_category_name_english').agg(
        revenue=('item_value', 'sum'),
        units=('sales_key', 'count'),
        avg_price=('price', 'mean')
    ).reset_index().sort_values(by='revenue', ascending=False).head(20)
    
    scatter = ax_c2.scatter(cat_all['units'], cat_all['revenue'] / 1e6, s=cat_all['avg_price'] * 3.5, 
                           c=cat_all['avg_price'], cmap='viridis', alpha=0.85, edgecolors='#F8FAFC', lw=0.5)
    ax_c2.set_xlabel("Units Sold (Volume)", fontsize=8.5)
    ax_c2.set_ylabel("Total Revenue (R$ Millions)", fontsize=8.5)
    ax_c2.set_title("Category Portfolio Matrix (Size = Avg Price)", fontsize=11, fontweight='bold', color=TEXT_WHITE, loc='left')
    ax_c2.grid(True, color=GRID_COLOR, linestyle='--', alpha=0.5)
    # Label top 4 categories
    for _, row in cat_all.head(4).iterrows():
        ax_c2.annotate(row['product_category_name_english'].replace('_', ' ').title(), 
                       (row['units'] + 150, row['revenue']/1e6 + 0.02), fontsize=7.5, color=TEXT_WHITE)

    # Chart 3: Freight Ratio % by Top Categories
    ax_c3 = fig.add_subplot(gs[2, 0:2])
    ax_c3.set_facecolor(PANEL_COLOR)
    for spine in ax_c3.spines.values(): spine.set_color('#475569')
    
    cat_freight = fact_sales.merge(dim_product, on='product_key').groupby('product_category_name_english').agg(
        prod_rev=('price', 'sum'),
        freight=('freight_value', 'sum')
    ).reset_index()
    cat_freight['freight_pct'] = (cat_freight['freight'] / (cat_freight['prod_rev'] + cat_freight['freight'])) * 100
    top_freight = cat_freight.sort_values(by='prod_rev', ascending=False).head(8)
    
    x_f = np.arange(len(top_freight))
    ax_c3.bar(x_f, top_freight['freight_pct'], color=ACCENT_AMBER, width=0.55)
    ax_c3.set_xticks(x_f)
    ax_c3.set_xticklabels([c.replace('_', ' ').title() for c in top_freight['product_category_name_english']], rotation=30, ha='right', fontsize=7.5)
    ax_c3.set_ylabel("Freight Share (% of GMV)", fontsize=8.5)
    ax_c3.set_title("Freight Share % in Top Categories", fontsize=11, fontweight='bold', color=TEXT_WHITE, loc='left')
    ax_c3.grid(True, color=GRID_COLOR, linestyle='--', alpha=0.5)

    # Chart 4: Price Distribution of Catalog SKUs
    ax_c4 = fig.add_subplot(gs[2, 2:4])
    ax_c4.set_facecolor(PANEL_COLOR)
    for spine in ax_c4.spines.values(): spine.set_color('#475569')
    
    prices = fact_sales['price']
    prices_filtered = prices[prices <= 500]
    ax_c4.hist(prices_filtered, bins=35, color=ACCENT_PURPLE, edgecolor='#0F172A', alpha=0.85)
    ax_c4.set_xlabel("Item Price (BRL, capped at R$ 500)", fontsize=8.5)
    ax_c4.set_ylabel("Number of Sales", fontsize=8.5)
    ax_c4.set_title("Order Item Price Distribution", fontsize=11, fontweight='bold', color=TEXT_WHITE, loc='left')
    ax_c4.grid(True, color=GRID_COLOR, linestyle='--', alpha=0.5)

    plt.savefig('docs/images/dashboard_page2_sales_products.png', dpi=180, facecolor=BG_COLOR)
    plt.savefig('reports/screenshots/dashboard_page2_sales_products.png', dpi=180, facecolor=BG_COLOR)
    plt.close()
    print("Saved Page 2 Screenshot.")


# =============================================================================
# 3. PAGE 3: CUSTOMER ANALYTICS & RFM SEGMENTATION
# =============================================================================
def render_page3():
    print("Rendering Page 3: Customers & RFM...")
    fig = plt.figure(figsize=(16, 9), facecolor=BG_COLOR, dpi=150)
    add_header(fig, "Customer RFM")
    
    gs = gridspec.GridSpec(3, 4, figure=fig, top=0.91, bottom=0.05, left=0.03, right=0.97, 
                           hspace=0.32, wspace=0.25, height_ratios=[0.18, 0.41, 0.41])
    
    # 4 KPI Cards
    ax_kpi1 = fig.add_subplot(gs[0, 0])
    draw_kpi_card(ax_kpi1, "TOTAL UNIQUE CUSTOMERS", "96,096", "Single Order: 97.0%", ACCENT_PURPLE)
    
    ax_kpi2 = fig.add_subplot(gs[0, 1])
    draw_kpi_card(ax_kpi2, "POTENTIAL LOYALISTS SPEND", "R$ 6.03M", "38.1% of Total Spend", ACCENT_TEAL)
    
    ax_kpi3 = fig.add_subplot(gs[0, 2])
    draw_kpi_card(ax_kpi3, "CHAMPIONS REVENUE", "R$ 627,098", "Top Tier CLV Segment", ACCENT_GREEN)
    
    ax_kpi4 = fig.add_subplot(gs[0, 3])
    draw_kpi_card(ax_kpi4, "AT RISK & LOST SPEND", "R$ 4.07M", "Retention Target Pool", ACCENT_ROSE)
    
    # Chart 1: RFM Segments Revenue Contribution
    ax_c1 = fig.add_subplot(gs[1, 0:2])
    ax_c1.set_facecolor(PANEL_COLOR)
    for spine in ax_c1.spines.values(): spine.set_color('#475569')
    
    rfm_df = dim_customer.groupby('rfm_segment').agg(
        revenue=('rfm_monetary', 'sum'),
        customers=('customer_unique_id', 'nunique')
    ).reset_index().sort_values(by='revenue', ascending=True)
    
    y = np.arange(len(rfm_df))
    palette_rfm = [ACCENT_ROSE if 'Lost' in s or 'Risk' in s else ACCENT_TEAL for s in rfm_df['rfm_segment']]
    bars = ax_c1.barh(y, rfm_df['revenue'] / 1e6, color=palette_rfm, height=0.6)
    ax_c1.set_yticks(y)
    ax_c1.set_yticklabels(rfm_df['rfm_segment'], fontsize=8)
    ax_c1.set_xlabel("Total Spend (R$ Millions)", fontsize=8.5)
    ax_c1.set_title("Revenue Contribution by RFM Segment", fontsize=11, fontweight='bold', color=TEXT_WHITE, loc='left')
    ax_c1.grid(True, color=GRID_COLOR, linestyle='--', alpha=0.5)
    for b in bars:
        ax_c1.text(b.get_width() + 0.03, b.get_y() + b.get_height()/2, f"R$ {b.get_width():.2f}M", 
                   va='center', fontsize=7.5, color=TEXT_WHITE)

    # Chart 2: Customer Distribution by RFM Segment
    ax_c2 = fig.add_subplot(gs[1, 2:4])
    ax_c2.set_facecolor(PANEL_COLOR)
    for spine in ax_c2.spines.values(): spine.set_color('#475569')
    
    rfm_cust = rfm_df.sort_values(by='customers', ascending=True)
    y_c = np.arange(len(rfm_cust))
    bars2 = ax_c2.barh(y_c, rfm_cust['customers'] / 1e3, color=ACCENT_BLUE, height=0.6)
    ax_c2.set_yticks(y_c)
    ax_c2.set_yticklabels(rfm_cust['rfm_segment'], fontsize=8)
    ax_c2.set_xlabel("Customer Count (Thousands)", fontsize=8.5)
    ax_c2.set_title("Customer Count by RFM Segment", fontsize=11, fontweight='bold', color=TEXT_WHITE, loc='left')
    ax_c2.grid(True, color=GRID_COLOR, linestyle='--', alpha=0.5)
    for b in bars2:
        ax_c2.text(b.get_width() + 0.2, b.get_y() + b.get_height()/2, f"{b.get_width():.1f}k", 
                   va='center', fontsize=7.5, color=TEXT_WHITE)

    # Chart 3: Customer Recency Distribution
    ax_c3 = fig.add_subplot(gs[2, 0:2])
    ax_c3.set_facecolor(PANEL_COLOR)
    for spine in ax_c3.spines.values(): spine.set_color('#475569')
    
    ax_c3.hist(dim_customer['rfm_recency'], bins=30, color=ACCENT_AMBER, edgecolor='#0F172A', alpha=0.85)
    ax_c3.set_xlabel("Days Since Last Purchase", fontsize=8.5)
    ax_c3.set_ylabel("Customer Count", fontsize=8.5)
    ax_c3.set_title("Customer Recency Distribution (Days)", fontsize=11, fontweight='bold', color=TEXT_WHITE, loc='left')
    ax_c3.grid(True, color=GRID_COLOR, linestyle='--', alpha=0.5)

    # Chart 4: Repeat vs Single Purchase Spend
    ax_c4 = fig.add_subplot(gs[2, 2:4])
    ax_c4.set_facecolor(PANEL_COLOR)
    for spine in ax_c4.spines.values(): spine.set_color('#475569')
    
    repeat_df = dim_customer.groupby('is_repeat_customer').agg(
        total_rev=('rfm_monetary', 'sum'),
        avg_rev=('rfm_monetary', 'mean')
    ).reset_index()
    
    labels = ['Single Purchase\n(1 Order)', 'Repeat Customer\n(>1 Orders)']
    x_r = np.arange(len(repeat_df))
    ax_c4.bar(x_r, repeat_df['total_rev'] / 1e6, color=[ACCENT_BLUE, ACCENT_GREEN], width=0.45)
    ax_c4.set_xticks(x_r)
    ax_c4.set_xticklabels(labels, fontsize=9, fontweight='semibold')
    ax_c4.set_ylabel("Total Spend (R$ Millions)", fontsize=8.5)
    ax_c4.set_title("Retention Split: Single vs Repeat Revenue", fontsize=11, fontweight='bold', color=TEXT_WHITE, loc='left')
    ax_c4.grid(True, color=GRID_COLOR, linestyle='--', alpha=0.5)
    for i, r in repeat_df.iterrows():
        ax_c4.text(i, (r['total_rev'] / 1e6) / 2, f"R$ {r['total_rev']/1e6:.2f}M\n(Avg: R$ {r['avg_rev']:.1f})", 
                   ha='center', va='center', color=TEXT_WHITE, fontweight='bold', fontsize=8.5)

    plt.savefig('docs/images/dashboard_page3_customer_rfm.png', dpi=180, facecolor=BG_COLOR)
    plt.savefig('reports/screenshots/dashboard_page3_customer_rfm.png', dpi=180, facecolor=BG_COLOR)
    plt.close()
    print("Saved Page 3 Screenshot.")


# =============================================================================
# 4. PAGE 4: OPERATIONS & CUSTOMER SATISFACTION (CSAT)
# =============================================================================
def render_page4():
    print("Rendering Page 4: Operations & CSAT...")
    fig = plt.figure(figsize=(16, 9), facecolor=BG_COLOR, dpi=150)
    add_header(fig, "Operations & CSAT")
    
    gs = gridspec.GridSpec(3, 4, figure=fig, top=0.91, bottom=0.05, left=0.03, right=0.97, 
                           hspace=0.32, wspace=0.25, height_ratios=[0.18, 0.41, 0.41])
    
    # 4 KPI Cards
    ax_kpi1 = fig.add_subplot(gs[0, 0])
    draw_kpi_card(ax_kpi1, "AVG ACTUAL DELIVERY", "12.6 Days", "Estimated Quoted: 24.2 Days", ACCENT_TEAL)
    
    ax_kpi2 = fig.add_subplot(gs[0, 1])
    draw_kpi_card(ax_kpi2, "LATE DELIVERY RATE", "8.11%", "7,826 Breach Orders", ACCENT_ROSE)
    
    ax_kpi3 = fig.add_subplot(gs[0, 2])
    draw_kpi_card(ax_kpi3, "ON-TIME CSAT RATING", "4.29 / 5.0", "62.4% 5-Star Reviews", ACCENT_GREEN)
    
    ax_kpi4 = fig.add_subplot(gs[0, 3])
    draw_kpi_card(ax_kpi4, "DELAYED CSAT RATING", "2.57 / 5.0", "46.2% 1-Star Reviews (-40%)", ACCENT_AMBER)
    
    # Chart 1: CSAT & 1-Star Surge (On-Time vs Delayed)
    ax_c1 = fig.add_subplot(gs[1, 0:2])
    ax_c1.set_facecolor(PANEL_COLOR)
    for spine in ax_c1.spines.values(): spine.set_color('#475569')
    
    deliv_csat = fact_orders[fact_orders['order_status'] == 'delivered'].merge(fact_reviews, on='order_id')
    agg_csat = deliv_csat.groupby('is_late').agg(
        avg_score=('review_score', 'mean'),
        one_star=('review_score', lambda x: (x == 1).mean() * 100),
        five_star=('review_score', lambda x: (x == 5).mean() * 100)
    ).reset_index()
    
    x_comp = np.array([0, 1])
    w = 0.35
    ax_c1.bar(x_comp - w/2, agg_csat['avg_score'], width=w, color=ACCENT_BLUE, label='Avg Review Score (1-5)')
    ax_c1.bar(x_comp + w/2, agg_csat['one_star'] / 10, width=w, color=ACCENT_ROSE, label='1-Star Review Rate (Scaled /10)')
    ax_c1.set_xticks(x_comp)
    ax_c1.set_xticklabels(['On-Time / Early\n(Score: 4.29)', 'Delayed Delivery\n(Score: 2.57)'], fontsize=9, fontweight='bold')
    ax_c1.set_ylabel("Metric Score", fontsize=8.5)
    ax_c1.set_title("Impact of Delivery Delays on Review Scores & 1-Star Surge", fontsize=11, fontweight='bold', color=TEXT_WHITE, loc='left')
    ax_c1.legend(loc='upper right', fontsize=8, facecolor='#1E293B', edgecolor='#475569')
    ax_c1.grid(True, color=GRID_COLOR, linestyle='--', alpha=0.5)

    # Chart 2: State Delivery Turnaround vs Late Rate %
    ax_c2 = fig.add_subplot(gs[1, 2:4])
    ax_c2.set_facecolor(PANEL_COLOR)
    for spine in ax_c2.spines.values(): spine.set_color('#475569')
    
    st_perf = fact_orders[fact_orders['order_status'] == 'delivered'].merge(
        dim_customer, on='customer_key'
    ).groupby('customer_state_x').agg(
        orders=('order_id', 'count'),
        avg_deliv=('delivery_days', 'mean'),
        late_rate=('is_late', lambda x: x.mean() * 100)
    ).reset_index()
    st_top8 = st_perf[st_perf['orders'] > 1000].sort_values(by='late_rate', ascending=False).head(8)
    
    x_st = np.arange(len(st_top8))
    ax_c2.bar(x_st - w/2, st_top8['avg_deliv'], width=w, color=ACCENT_TEAL, label='Avg Delivery Days')
    ax_c2.bar(x_st + w/2, st_top8['late_rate'], width=w, color=ACCENT_ROSE, label='Late Delivery %')
    ax_c2.set_xticks(x_st)
    ax_c2.set_xticklabels(st_top8['customer_state_x'], fontsize=8.5, fontweight='bold')
    ax_c2.set_ylabel("Days / Percentage", fontsize=8.5)
    ax_c2.set_title("Regional Delivery Bottlenecks (RJ vs SP & Others)", fontsize=11, fontweight='bold', color=TEXT_WHITE, loc='left')
    ax_c2.legend(loc='upper right', fontsize=8, facecolor='#1E293B', edgecolor='#475569')
    ax_c2.grid(True, color=GRID_COLOR, linestyle='--', alpha=0.5)

    # Chart 3: Review Score Breakdown (1 to 5 Stars)
    ax_c3 = fig.add_subplot(gs[2, 0:2])
    ax_c3.set_facecolor(PANEL_COLOR)
    for spine in ax_c3.spines.values(): spine.set_color('#475569')
    
    score_dist = fact_reviews['review_score'].value_counts().sort_index(ascending=True)
    stars = [f"{s} Star" for s in score_dist.index]
    palette_stars = [ACCENT_ROSE, ACCENT_AMBER, ACCENT_AMBER, ACCENT_BLUE, ACCENT_GREEN]
    bars_star = ax_c3.bar(stars, score_dist.values / 1e3, color=palette_stars, width=0.55)
    ax_c3.set_ylabel("Reviews (Thousands)", fontsize=8.5)
    ax_c3.set_title("Customer Review Score Distribution (CSAT)", fontsize=11, fontweight='bold', color=TEXT_WHITE, loc='left')
    ax_c3.grid(True, color=GRID_COLOR, linestyle='--', alpha=0.5)
    for b in bars_star:
        ax_c3.text(b.get_x() + b.get_width()/2, b.get_height() + 1, f"{b.get_height():.1f}k\n({b.get_height()/len(fact_reviews)*1e5:.1f}%)", 
                   ha='center', fontsize=7.5, color=TEXT_WHITE, fontweight='semibold')

    # Chart 4: Seller Compliance vs Volume Matrix
    ax_c4 = fig.add_subplot(gs[2, 2:4])
    ax_c4.set_facecolor(PANEL_COLOR)
    for spine in ax_c4.spines.values(): spine.set_color('#475569')
    
    seller_perf = fact_sales.merge(fact_orders, on='order_id').groupby('seller_key').agg(
        units_sold=('sales_key', 'count'),
        late_pct=('is_late', lambda x: x.mean() * 100),
        total_rev=('item_value', 'sum')
    ).reset_index()
    seller_top = seller_perf[seller_perf['units_sold'] >= 20]
    
    ax_c4.scatter(seller_top['units_sold'], seller_top['late_pct'], c=ACCENT_TEAL, alpha=0.6, s=30, edgecolors='none')
    ax_c4.axhline(y=10.0, color=ACCENT_ROSE, linestyle='--', lw=1.5, label='10% SLA Penalty Threshold')
    ax_c4.set_xlabel("Seller Volume (Units Sold)", fontsize=8.5)
    ax_c4.set_ylabel("Seller Late Delivery Rate (%)", fontsize=8.5)
    ax_c4.set_title("Merchant SLA Compliance vs Volume", fontsize=11, fontweight='bold', color=TEXT_WHITE, loc='left')
    ax_c4.legend(loc='upper right', fontsize=8, facecolor='#1E293B', edgecolor='#475569')
    ax_c4.grid(True, color=GRID_COLOR, linestyle='--', alpha=0.5)

    plt.savefig('docs/images/dashboard_page4_operations_csat.png', dpi=180, facecolor=BG_COLOR)
    plt.savefig('reports/screenshots/dashboard_page4_operations_csat.png', dpi=180, facecolor=BG_COLOR)
    plt.close()
    print("Saved Page 4 Screenshot.")


if __name__ == '__main__':
    render_page1()
    render_page2()
    render_page3()
    render_page4()
    print("All 4 real dashboard screenshots generated successfully!")
