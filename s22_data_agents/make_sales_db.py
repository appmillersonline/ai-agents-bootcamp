"""Build sales.db: three months of made-up sales for Sara's shop (fixed seed, so everyone gets the same data)."""
import random
import sqlite3
from datetime import date, timedelta

random.seed(7)
PRODUCTS = [("Blue mug set", "Kitchen", 24.0), ("Candle trio", "Home", 18.5), ("Linen tote bag", "Bags", 15.0),
            ("Ceramic vase", "Home", 32.0), ("Tea towel", "Kitchen", 9.0), ("Lavender candle", "Home", 12.0)]
CHANNELS = ["website", "market stall", "wholesale"]

db = sqlite3.connect("sales.db")
db.executescript("""
DROP TABLE IF EXISTS products; DROP TABLE IF EXISTS orders;
CREATE TABLE products (product_id INTEGER PRIMARY KEY, name TEXT, category TEXT, price_eur REAL);
CREATE TABLE orders (order_id INTEGER PRIMARY KEY, order_date TEXT, product_id INTEGER, qty INTEGER,
                     channel TEXT, discount_pct INTEGER);
""")
db.executemany("INSERT INTO products VALUES (?, ?, ?, ?)", [(i + 1, *p) for i, p in enumerate(PRODUCTS)])
oid, day = 2000, date(2026, 8, 1)
while day <= date(2026, 10, 31):
    busy = 6 if day.weekday() >= 5 else 3                    # weekends are busier
    for _ in range(random.randint(busy - 2, busy + 2)):
        pid = random.choices(range(1, 7), weights=[3, 4, 3, 1, 4, 3])[0]
        channel = random.choices(CHANNELS, weights=[6, 3, 1])[0]
        qty = random.randint(5, 20) if channel == "wholesale" else random.randint(1, 3)
        disc = 10 if channel == "wholesale" else random.choice([0, 0, 0, 0, 15])
        if pid == 2 and day.month == 10:                     # candle trio takes off in October
            qty += 1
        db.execute("INSERT INTO orders VALUES (?, ?, ?, ?, ?, ?)", (oid, day.isoformat(), pid, qty, channel, disc))
        oid += 1
    day += timedelta(days=1)
db.commit()
print("orders:", db.execute("SELECT COUNT(*) FROM orders").fetchone()[0])
