"""Trust, but check: add up the sales with plain Python and compare with Claude's numbers."""
import csv
from collections import Counter

from common import DATA

revenue, days = Counter(), Counter()
with open(DATA / "october_sales.csv", newline="") as f:
    for row in csv.DictReader(f):
        money = int(row["qty"]) * float(row["price_eur"])
        revenue[row["item"]] += money
        days[row["weekday"]] += money

for item, total in revenue.most_common(3):
    print(f"{item:<16} €{total:,.0f}")
print(f"Best day: {days.most_common(1)[0][0]}, total €{sum(revenue.values()):,.0f}")
