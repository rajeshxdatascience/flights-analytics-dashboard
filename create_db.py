import pandas as pd
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "data", "new_flights.csv")
DB_PATH = os.path.join(BASE_DIR, "flights.db")

print("CSV PATH:", CSV_PATH)
print("DB PATH:", DB_PATH)

df = pd.read_csv(CSV_PATH)

conn = sqlite3.connect(DB_PATH)
df.to_sql("new_flights", conn, if_exists="replace", index=False)
conn.close()

print("✅ Database & table created successfully")
print("Rows inserted:", len(df))
