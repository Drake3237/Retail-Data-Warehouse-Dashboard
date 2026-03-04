import pandas as pd
import sqlite3


def load_dimensions():

    conn = sqlite3.connect("retail_warehouse.db")

    # -------------------------
    # LOAD RAW DATA FILES
    # -------------------------

    stores = pd.read_csv("data/raw_stores.csv")
    products = pd.read_csv("data/raw_products.csv")
    customers = pd.read_csv("data/raw_customers.csv")
    transactions = pd.read_csv("data/raw_transactions.csv")

    print("Files loaded successfully.")
    print("Transaction columns detected:")
    print(transactions.columns)

    # -------------------------
    # LOAD STORE DIMENSION
    # -------------------------

    stores_dim = stores.copy()
    stores_dim.to_sql("dim_store", conn, if_exists="replace", index=False)

    # -------------------------
    # LOAD PRODUCT DIMENSION
    # -------------------------

    products_dim = products.copy()
    products_dim.to_sql("dim_product", conn, if_exists="replace", index=False)

    # -------------------------
    # LOAD CUSTOMER DIMENSION
    # -------------------------

    customers_dim = customers.copy()
    customers_dim.to_sql("dim_customer", conn, if_exists="replace", index=False)

    # -------------------------
    # CREATE DATE DIMENSION
    # -------------------------

    # Detect date column automatically
    possible_date_cols = ["date", "transaction_date", "sale_date", "order_date"]

    date_column = None
    for col in possible_date_cols:
        if col in transactions.columns:
            date_column = col
            break

    if date_column is None:
        raise Exception(
            "No recognizable date column found in raw_transactions.csv.\n"
            "Check the column names printed above."
        )

    transactions["full_date"] = pd.to_datetime(transactions[date_column])

    date_dim = transactions[["full_date"]].drop_duplicates().copy()

    date_dim["date_id"] = date_dim["full_date"].dt.strftime("%Y%m%d").astype(int)
    date_dim["day"] = date_dim["full_date"].dt.day
    date_dim["month"] = date_dim["full_date"].dt.month
    date_dim["year"] = date_dim["full_date"].dt.year
    date_dim["quarter"] = date_dim["full_date"].dt.quarter

    date_dim = date_dim[
        ["date_id", "full_date", "day", "month", "year", "quarter"]
    ]

    date_dim.to_sql("dim_date", conn, if_exists="replace", index=False)

    conn.close()

    print("Dimension tables loaded successfully.")


if __name__ == "__main__":
    load_dimensions()