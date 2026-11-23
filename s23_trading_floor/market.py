"""A made-up market for the capstone: five fictional companies, 30 days of simulated prices and news. Not real stocks."""
import os
import random

COMPANIES = {
    "CLAY": "Clayworks Group, handmade ceramics",
    "WICK": "Wick & Co, candles and home scents",
    "LOOM": "Northloom, woven textiles",
    "TIDE": "Tideway Freight, shipping and parcels",
    "NOVA": "Nova Kilns, energy-saving kilns",
}
START = {"CLAY": 40.0, "WICK": 25.0, "LOOM": 18.0, "TIDE": 55.0, "NOVA": 12.0}
TREND = {"CLAY": 0.004, "WICK": 0.010, "LOOM": -0.006, "TIDE": 0.001, "NOVA": 0.018}
NEWS = {
    "CLAY": [(24, "Clayworks opens a second studio; orders up 12 percent.")],
    "WICK": [(27, "Wick & Co signs a deal with a national gift chain.")],
    "LOOM": [(22, "Northloom warns of higher cotton costs this winter."), (29, "Northloom's CEO steps down.")],
    "TIDE": [(28, "Tideway Freight says parcel volumes are flat.")],
    "NOVA": [(25, "Nova Kilns wins an energy award; shares jump."), (30, "Analysts call Nova Kilns 'priced for perfection'.")],
}
DAYS = 30
TODAY = int(os.environ.get("MARKET_DAY", DAYS))         # which day of the simulation it is

random.seed(23)
PRICES = {}
for t in COMPANIES:
    p, series = START[t], []
    for _ in range(DAYS):
        p *= 1 + TREND[t] + random.gauss(0, 0.02)
        series.append(round(p, 2))
    PRICES[t] = series


def price_today(ticker: str) -> float:
    return PRICES[ticker][TODAY - 1]


def history(ticker: str) -> list[float]:
    return PRICES[ticker][:TODAY]
