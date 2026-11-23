import csv
from collections import defaultdict, Counter
from datetime import datetime

sizes_revenue = defaultdict(float)
day_revenue = defaultdict(float)
scents_qty = Counter()
total_revenue = 0.0

with open('sales.csv', newline='', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        date_str = row['date']
        size = row['size']
        scent = row['scent']
        quantity = int(row['quantity'])
        price = float(row['price'])
        revenue = quantity * price

        total_revenue += revenue
        sizes_revenue[size] += revenue
        day_name = datetime.strptime(date_str, '%Y-%m-%d').strftime('%A')
        day_revenue[day_name] += revenue
        scents_qty[scent] += quantity

best_day = max(day_revenue.items(), key=lambda x: (x[1], x[0]))
top_3_scents = scents_qty.most_common(3)

print(f'Total revenue: ${total_revenue:.2f}')
print('Revenue by size:')
for size in sorted(sizes_revenue):
    print(f'  {size}: ${sizes_revenue[size]:.2f}')
print(f'Best day of the week by revenue: {best_day[0]} (${best_day[1]:.2f})')
print('Top 3 scents by quantity sold:')
for scent, qty in top_3_scents:
    print(f'  {scent}: {qty}')
