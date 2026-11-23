"""The trading floor at a glance: every trader's cash, holdings and value against the 10,000 they started with."""
import accounts

print(f"day {accounts.TODAY}")

for trader in ["Mia", "Vic", "Cora"]:
    p = accounts.portfolio(trader)
    holdings = ", ".join(f"{n} {t}" for t, n in p["holdings"].items()) or "nothing"
    print(f"{trader:<5} value {p['value']:>9,.2f}  ({p['value'] - accounts.START_CASH:+8,.2f})  cash {p['cash']:>9,.2f}  holds {holdings}")
