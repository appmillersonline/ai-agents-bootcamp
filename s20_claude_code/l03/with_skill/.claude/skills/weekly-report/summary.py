"""Weekly numbers from orders.csv: revenue, orders, items sold, best seller."""
import csv
import sys
from collections import Counter

rows = list(csv.DictReader(open(sys.argv[1])))
revenue = sum(int(r["qty"]) * float(r["price"]) for r in rows)
items = Counter()
for r in rows:
    items[r["item"]] += int(r["qty"])
best, sold = items.most_common(1)[0]
print(f"revenue: {revenue:.2f} EUR")
print(f"orders: {len(rows)}")
print(f"items sold: {sum(items.values())}")
print(f"best seller: {best} ({sold} sold)")
