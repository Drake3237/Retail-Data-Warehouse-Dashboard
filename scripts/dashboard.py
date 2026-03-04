
import streamlit as st
import pandas as pd
import sqlite3

st.set_page_config(page_title="Retail Warehouse Dashboard", layout="wide")

st.title ("Retail Warehouse Analytics Dashboard")



# Connect to the database

conn = sqlite3.connect("retail_warehouse.db")


regions = pd.read_sql_query("""
    SELECT DISTINCT region
    FROM dim_store
""", conn)
region_list = regions["region"].tolist()

selected_region = st.selectbox("Select Region", ["All"] + region_list)




# Load Data for Dashboard

if selected_region == "All":
        revenue_query = """
            SELECT s.region, SUM(f.total_amount) AS revenue
            FROM fact_sales f
            JOIN dim_store s ON f.store_id = s.store_id
            GROUP BY s.region
            ORDER BY revenue DESC
        """
else: 
        revenue_query = f"""
            SELECT s.region, SUM(f.total_amount) AS revenue
            FROM fact_sales f
            JOIN dim_store s ON f.store_id = s.store_id
            WHERE s.region = '{selected_region}'
            GROUP BY s.region
            ORDER BY revenue DESC
        """

revenue_by_region = pd.read_sql_query(revenue_query, conn)


monthly_revenue = pd.read_sql_query("""
    SELECT d.year, d.month, SUM(f.total_amount) AS revenue
    FROM fact_sales f
    JOIN dim_date d ON f.date_id = d.date_id
    GROUP BY d.year, d.month
    ORDER BY d.year, d.month
""",conn)

# Profit by Product Data 

profit_data = pd.read_sql_query("""
    SELECT 
        p.product_name,
        SUM(f.quantity * p.price) AS revenue,
        SUM(f.quantity * p.cost) AS cost,
        SUM(f.quantity * p.price) - SUM(f.quantity * p.cost) AS profit
    FROM fact_sales f
    JOIN dim_product p ON f.product_id = p.product_id
    GROUP BY p.product_name
    ORDER BY profit DESC
""", conn)

conn.close()



# KPIs and Metrics 
total_profit = profit_data["profit"].sum()
total_revenue = profit_data["revenue"].sum()
margin = (total_profit / total_revenue) * 100 if total_revenue > 0 else 0

col4 = st.columns(1)[0]
col4.metric("Total Profit", f"${total_profit:,.2f}", f"{margin:.2f}% margin")



total_revenue = revenue_by_region["revenue"].sum()

total_orders_query = """
    SELECT COUNT(*) AS total_orders
    FROM fact_sales
"""

conn = sqlite3.connect("retail_warehouse.db")
total_orders = pd.read_sql_query(total_orders_query, conn).iloc[0,0]
conn.close()

col1, col2 = st.columns(2)

col1.metric("Total Revenue", f"${total_revenue:,.2f}")
col2.metric("Total Orders", f"{total_orders:,}")


# Show Tables / Data
st.subheader("Revenue by Region")
st.bar_chart(revenue_by_region.set_index("region"))

st.subheader("Monthly Revenue")
st.line_chart(monthly_revenue["revenue"])

st.subheader("Top Profitable Products")
st.bar_chart(profit_data.set_index("product_name")["profit"].head(10))