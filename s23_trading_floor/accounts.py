"""Simulated trading accounts in SQLite. Fake money only. The rules live here, in code, not in the prompts."""
import sqlite3
from pathlib import Path

from market import COMPANIES, TODAY, price_today

DB = Path(__file__).parent / "accounts.db"
START_CASH = 10_000.0
MAX_POSITION = 0.30                                   # no single company above 30% of a portfolio
MIN_CASH = {"Cora": 0.50}                             # Cora's style, enforced: keep half in cash


def db():
    con = sqlite3.connect(DB)
    con.executescript("""CREATE TABLE IF NOT EXISTS cash (trader TEXT PRIMARY KEY, amount REAL);
        CREATE TABLE IF NOT EXISTS holdings (trader TEXT, ticker TEXT, shares INTEGER, PRIMARY KEY (trader, ticker));
        CREATE TABLE IF NOT EXISTS trades (day INTEGER, trader TEXT, side TEXT, ticker TEXT, shares INTEGER, price REAL, reason TEXT);
        CREATE TABLE IF NOT EXISTS values_by_day (day INTEGER, trader TEXT, value REAL, PRIMARY KEY (day, trader));""")
    return con


def open_account(trader: str) -> None:
    with db() as con:
        con.execute("INSERT OR IGNORE INTO cash VALUES (?, ?)", (trader, START_CASH))


def portfolio(trader: str) -> dict:
    con = db()
    cash = con.execute("SELECT amount FROM cash WHERE trader = ?", (trader,)).fetchone()[0]
    holdings = dict(con.execute("SELECT ticker, shares FROM holdings WHERE trader = ? AND shares > 0", (trader,)))
    value = cash + sum(n * price_today(t) for t, n in holdings.items())
    return {"cash": round(cash, 2), "holdings": holdings, "value": round(value, 2)}


def trade(trader: str, side: str, ticker: str, shares: int, reason: str) -> str:
    ticker = ticker.upper()
    if ticker not in COMPANIES or shares <= 0:
        return "Rejected: unknown company or zero shares."
    p, price = portfolio(trader), price_today(ticker)
    held = p["holdings"].get(ticker, 0)
    if side == "buy":
        if shares * price > p["cash"]:
            return f"Rejected: costs {shares * price:.2f}, but only {p['cash']:.2f} cash."
        if (held + shares) * price > MAX_POSITION * p["value"]:
            return f"Rejected: {ticker} would be above 30% of the portfolio (max {int(MAX_POSITION * p['value'] / price) - held} more shares)."
        if p["cash"] - shares * price < MIN_CASH.get(trader, 0) * p["value"]:
            return f"Rejected: {trader} must keep {MIN_CASH[trader]:.0%} of the portfolio in cash."
    elif shares > held:
        return f"Rejected: you only hold {held} {ticker}."
    sign = 1 if side == "buy" else -1
    with db() as con:
        con.execute("UPDATE cash SET amount = amount - ? WHERE trader = ?", (sign * shares * price, trader))
        con.execute("INSERT INTO holdings VALUES (?, ?, ?) ON CONFLICT DO UPDATE SET shares = shares + ?",
                    (trader, ticker, sign * shares, sign * shares))
        con.execute("INSERT INTO trades VALUES (?, ?, ?, ?, ?, ?, ?)", (TODAY, trader, side, ticker, shares, price, reason))
    return f"Done: {side} {shares} {ticker} at {price:.2f}."


def snapshot(trader: str) -> None:
    """Record today's portfolio value, for the dashboard."""
    with db() as con:
        con.execute("INSERT OR REPLACE INTO values_by_day VALUES (?, ?, ?)", (TODAY, trader, portfolio(trader)["value"]))
