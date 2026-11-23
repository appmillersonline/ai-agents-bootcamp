"""MCP server: the made-up market. Companies, price history and news. Read-only."""
from mcp.server.fastmcp import FastMCP

from market import COMPANIES, NEWS, TODAY, history, price_today

mcp = FastMCP("market", log_level="WARNING")


@mcp.tool()
def list_companies() -> str:
    """List the five companies on this simulated market, with today's price."""
    return f"Day {TODAY}.\n" + "\n".join(f"{t}: {name}, today {price_today(t):.2f}" for t, name in COMPANIES.items())


@mcp.tool()
def price_history(ticker: str, days: int = 10) -> str:
    """Closing prices for the last few days, oldest first, plus the change over that period.

    Args:
        ticker: One of CLAY, WICK, LOOM, TIDE, NOVA.
        days: How many days back, at most 30.
    """
    s = history(ticker.upper())[-days:]
    return f"{ticker.upper()} last {len(s)} days: {', '.join(f'{p:.2f}' for p in s)} (change {100 * (s[-1] / s[0] - 1):+.1f}%)"


@mcp.tool()
def news(ticker: str) -> str:
    """Recent news headlines for one company, with the day they came out. Only news up to today."""
    items = [(d, h) for d, h in NEWS.get(ticker.upper(), []) if d <= TODAY]
    return "\n".join(f"day {d}: {h}" for d, h in items) or "No recent news."


if __name__ == "__main__":
    mcp.run()
