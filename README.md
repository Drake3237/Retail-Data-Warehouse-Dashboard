# 🏬 Retail Store Chain Data Warehouse & Analytics Dashboard

An end-to-end data engineering and analytics project simulating a retail store chain.

## 🚀 Project Overview

This project demonstrates:

- Synthetic and random retail data generation
- Star schema data warehouse design
- ETL pipeline automation
- SQL-based business analytics
- Interactive Streamlit dashboard
- Revenue, Profit, and Margin analysis

## 🏗 Architecture

1. Generate synthetic data (products, stores, customers, sales)
2. Build SQLite star schema warehouse
3. Load fact and dimension tables
4. Run analytics queries
5. Serve interactive dashboard with Streamlit

## 📊 Features

- Revenue by region
- Monthly revenue trends
- Top profitable products
- KPI metrics (Revenue, Transactions, Customers)
- Profit margin analysis
- Region filtering

## 🛠 Tech Stack

- Python
- SQLite
- Pandas
- Streamlit
- Faker
- Matplotlib

## ▶ How To Run

```bash
pip install -r requirements.txt
python scripts/run_pipeline.py
streamlit run scripts/dashboard.py