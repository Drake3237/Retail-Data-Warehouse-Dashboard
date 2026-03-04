import pandas as pd
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

# Settings -------------------
NUM_STORES = 10
NUM_PRODUCTS = 50
NUM_CUSTOMERS = 200
NUM_transactions = 5000



# Generate Stores -------------------

stores = []
for i in range(1, NUM_STORES + 1):
    stores.append ({
        'store_id': i,
        'store_name': f'{fake.city()} Retail',
        'state': fake.state(),
        'region': random.choice(['North', 'South', 'East', 'West'])
    })
    
df_stores = pd.DataFrame(stores)

# Generate Products -------------------

products = []

for i in range(1, NUM_PRODUCTS + 1):

    price = round(random.uniform(5.0, 500.0), 2)

    # Simulate realistic retail margin (20% to 60%)
    margin_pct = random.uniform(0.2, 0.6)

    cost = round(price * (1 - margin_pct), 2)

    products.append({
        'product_id': i,
        'product_name': fake.word().capitalize(),
        'category': random.choice(['Electronics', 'Clothing', 'Home', 'Sports']),
        'price': price,
        'cost': cost
    })

df_products = pd.DataFrame(products)

# Generate Customers -------------------

customers = []
for i in range(1, NUM_CUSTOMERS + 1):
    customers.append({
        'customer_id': i,   
        'customer_name': fake.name(),
        'email': fake.email(),
        'join_date': fake.date_between(start_date='-5y', end_date='today')
    })

df_customers = pd.DataFrame(customers)


# Generate Transactions -------------------

transactions = []

start_date = datetime(2023, 1, 1)

for i in range(1, NUM_transactions + 1):
    product = df_products.sample(1).iloc[0]
    quantity = random.randint(1, 5)


    transactions.append({
        'transaction_id': i,
        'store_id': random.randint(1, NUM_STORES),
        'product_id': product["product_id"],
        'customer_id': random.randint(1, NUM_CUSTOMERS),
        'quantity': quantity,
        'total_amount': round(quantity * product['price'], 2),
        'transaction_date': start_date + timedelta(days=random.randint(0, 730))
    })

df_transactions = pd.DataFrame(transactions)

# Save to CSV -------------------

df_stores.to_csv('data/raw_stores.csv', index=False)
df_products.to_csv('data/raw_products.csv', index=False)
df_customers.to_csv('data/raw_customers.csv', index=False)
df_transactions.to_csv('data/raw_transactions.csv', index=False)

print ("Raw generated data saved to the 'data/' directory successfully.")


