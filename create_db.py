import pandas as pd
import sqlite3
import os

print("Working directory:", os.getcwd())

df = pd.read_csv(r"C:\Users\rajes\CampusXDSMP1.0\Making a flight dashboard using python and sql\new_flights.csv")

conn = sqlite3.connect("flights.db")
df.to_sql("new_flights", conn, if_exists="replace", index=False)
conn.close()

print("✅ Database & table created successfully")
print("Rows inserted:", len(df))
