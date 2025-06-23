import pandas as pd
import sqlite3
import os

# DAta to load
DB_NAME = "mlb_data.db"
HISTORY_CSV = "clean_world_series_history.csv"
RECEIPTS_CSV = "clean_world_series_receipts.csv"

# Load cleaned CSVs
df_history = pd.read_csv(HISTORY_CSV)
df_receipts = pd.read_csv(RECEIPTS_CSV)

# Creating SQLite DB
conn = sqlite3.connect(DB_NAME)

# Tables
try:
    df_history.to_sql("series_history", conn, if_exists="replace", index=False)
    df_receipts.to_sql("gate_receipts", conn, if_exists="replace", index=False)
except Exception as e:
    print("Error writing to SQLite:", e)
    conn.close()
    exit(1)

# Checking sample data
print(df_history.head(5).to_markdown(index=False))

print(df_receipts.head(5).to_markdown(index=False))

# Close connection
conn.close()

