import csv
from pathlib import Path

path = Path("data/orders.csv")

with open(path) as f:
    for row in csv.DictReader(f):
        print(row["order_id"], row["customer"], row["status"])
