import sqlite3
import pandas as pd 

def run_analytics():

    conn = sqlite3.connect("retail_warehouse.db")

    # Total Revenue 

    total_revenue = pd.read_sql_query("""
        SELECT SUM(total_amount) AS total_revenue
        FROM fact_sales
    """, conn)

    print ("\n TOTAL REVENUE")
    print (total_revenue)


    # Revenue by Region

    revenue_by_region = pd.read_sql_query("""
    SELECT s.region, SUM(f.total_amount) AS revenue
    FROM fact_sales f
    JOIN dim_store s ON f.store_id = s.store_id
    GROUP BY s.region
    ORDER BY revenue DESC
    """, conn)

    print ("\n REVENUE BY REGION")
    print (revenue_by_region)

    # Revenue by Category

    revenue_by_category = pd.read_sql_query("""
    SELECT p.category, SUM(f.total_amount) AS revenue
    FROM fact_sales f
    JOIN dim_product p ON f.product_id = p.product_id
    GROUP BY p.category
    ORDER BY revenue DESC
    """, conn)

    print ("\n REVENUE BY CATEGORY")
    print (revenue_by_category)


    # Monthly Revenue Trend

    monthly_revenue = pd.read_sql_query("""
    SELECT d.year, d.month, SUM(f.total_amount) AS revenue
    FROM fact_sales f
    JOIN dim_date d ON f.date_id = d.date_id
    GROUP BY d.year, d.month
    ORDER BY d.year, d.month
    """, conn) 
    
    print ("\n MONTHLY REVENUE TREND")
    print (monthly_revenue)


    # Top 10 products by revenue

    top_products = pd.read_sql_query("""
    SELECT p.product_name, SUM(f.total_amount) AS revenue
    FROM fact_sales f
    JOIN dim_product p ON f.product_id = p.product_id
    GROUP BY p.product_name
    ORDER BY revenue DESC
    LIMIT 10
    """, conn)

    print ("\n TOP 10 PRODUCTS BY REVENUE")
    print (top_products)


    # Total Revenue KPI
    total_revenue = revenue_by_region['revenue'].sum()

    # Average Order Value
    avg_order_value = pd.read_sql_query("""
    SELECT AVG(total_amount) AS avg_order_value
    FROM fact_sales
    """, conn)

    # Total Orders
    total_orders = pd.read_sql_query("""
    SELECT COUNT(*) AS total_orders
    FROM fact_sales
    """, conn)

    print("\n===== BUSINESS KPIs =====")
    print(f"Total Revenue: ${total_revenue:,.2f}")
    print(f"Average Order Value: ${avg_order_value.iloc[0,0]:,.2f}")
    print(f"Total Orders: {total_orders.iloc[0,0]:,}")

    # Revenue Growth %
    monthly_revenue['prev_revenue'] = monthly_revenue['revenue'].shift(1)
    monthly_revenue['growth_pct'] = (
    (monthly_revenue['revenue'] - monthly_revenue['prev_revenue'])
    / monthly_revenue['prev_revenue']
    ) * 100

    print("\nMonthly Growth %:")
    print(monthly_revenue[['year','month','growth_pct']])



    conn.close()


if __name__ == "__main__":
    run_analytics()

                                          
