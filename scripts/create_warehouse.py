import sqlite3

conn = sqlite3.connect('retail_warehouse.db')
cursor = conn.cursor()



# Dimensions of the Warehouse

cursor.execute('''
CREATE TABLE IF NOT EXISTS dim_store (
    store_id INTEGER PRIMARY KEY, 
    Store_name TEXT,
    STATE TEXT,
    REGION TEXT
)
''')

cursor.execute('''

CREATE TABLE IF NOT EXISTS dim_product (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT,
    category TEXT,
    price REAL,
    cost REAL
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS dim_customer (
    customer_id INTEGER PRIMARY KEY, 
    customer_name TEXT,
    email TEXT,
    join_date DATE
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS dim_date (
    date_id INTEGER PRIMARY KEY,
    full_date DATE,
    day INTEGER,
    month INTEGER,
    year INTEGER,
    quarter INTEGER
)
''')


# Fact Table


cursor.execute('''
CREATE TABLE IF NOT EXISTS fact_sales (
    transaction_id INTEGER PRIMARY KEY,
    store_id INTEGER,
    product_id INTEGER,
    customer_id INTEGER,
    date_id INTEGER,
    quantity INTEGER,
    total_amount REAL,
    FOREIGN KEY (store_id) REFERENCES dim_store(store_id),
    FOREIGN KEY (product_id) REFERENCES dim_product(product_id),
    FOREIGN KEY (customer_id) REFERENCES dim_customer(customer_id),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
)
''')


conn.commit()
conn.close()

print("Warehouse Table created successfully.")

