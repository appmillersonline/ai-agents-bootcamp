"""B10: check the analyst's numbers ourselves, straight from the database with pandas. No model involved."""
import sqlite3
from pathlib import Path

import pandas as pd

con = sqlite3.connect(Path(__file__).parent / "sales.db")
df = pd.read_sql("SELECT o.*, p.name, p.price_eur FROM orders o JOIN products p USING(product_id)", con)
df["revenue"] = df.qty * df.price_eur * (100 - df.discount_pct) / 100
df["month"] = df.order_date.str[:7]

print("revenue by month:")
print(df.groupby("month").revenue.sum().round(2).to_string())
print("\ntop product each month:")
top = df.groupby(["month", "name"]).revenue.sum().round(2).reset_index()
print(top.loc[top.groupby("month").revenue.idxmax()].to_string(index=False))
print("\nrevenue by channel:")
print(df.groupby("channel").revenue.sum().round(2).sort_values(ascending=False).to_string())
