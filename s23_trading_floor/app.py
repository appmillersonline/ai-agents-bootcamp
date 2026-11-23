"""Ship it: a small FastAPI backend for the trading floor. JSON for any front end, plus a live page."""
import sqlite3
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse

HERE = Path(__file__).parent
app = FastAPI(title="AI Trading Floor (simulated)")


def query(sql: str) -> list[dict]:
    con = sqlite3.connect(f"file:{HERE / 'accounts.db'}?mode=ro", uri=True)   # the web app only reads
    con.row_factory = sqlite3.Row
    return [dict(r) for r in con.execute(sql)]


@app.get("/api/floor")
def floor() -> dict:
    """Everything the front end needs: values per day, and the latest trades."""
    return {
        "simulated": True,
        "history": query("SELECT day, trader, value FROM values_by_day ORDER BY day"),
        "trades": query("SELECT day, trader, side, ticker, shares, reason FROM trades ORDER BY rowid DESC LIMIT 6"),
    }


@app.get("/")
def page():
    return FileResponse(HERE / "static" / "index.html")
