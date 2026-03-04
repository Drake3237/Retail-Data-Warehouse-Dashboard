import pandas as pd 
import sqlite3


def load_fact_table():

    conn = sqlite3.connect("retail_warehouse.db")

    transactions = pd.read_csv("data/raw_transactions.csv")

    print ("Transaction file loaded successfully.")
    print ("Transaction columns detected:", transactions.columns)

    #Detect date column automatically
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
    
    # Create date dimension entries
    transactions["date_id"] = pd.to_datetime(transactions[date_column]).dt.strftime("%Y%m%d").astype(int)

    # select only the necessary columns for the fact table

    fact_sales = transactions[
        ["transaction_id",
        "store_id",
        "product_id",
        "customer_id",
        "date_id",
        "quantity",
        "total_amount"
        ]
    ]

    fact_sales.to_sql("fact_sales", conn, if_exists="replace", index=False)

    conn.close()
    print("Fact table loaded successfully.")


if __name__ == "__main__":
    load_fact_table()



