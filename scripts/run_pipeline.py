import os

os.system("python scripts/create_warehouse.py")
os.system("python scripts/generate_data.py")
os.system("python scripts/load_dimensions.py")
os.system("python scripts/load_fact_table.py")
os.system("python scripts/run_analytics.py")

print ("\nData extraction, generation, and loading completed successfully.")

