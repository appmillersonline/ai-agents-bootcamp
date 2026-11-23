"""MCP server: simulated accounts. See your portfolio, buy and sell with fake money. Rules enforced in accounts.py."""
from mcp.server.fastmcp import FastMCP

import accounts

mcp = FastMCP("accounts", log_level="WARNING")


@mcp.tool()
def get_portfolio(trader: str) -> str:
    """Your cash, your holdings and your total portfolio value (simulated money)."""
    accounts.open_account(trader)
    return str(accounts.portfolio(trader))


@mcp.tool()
def buy_shares(trader: str, ticker: str, shares: int, reason: str) -> str:
    """Buy shares with simulated cash. No company may go above 30% of your portfolio.

    Args:
        trader: Your own name.
        ticker: One of CLAY, WICK, LOOM, TIDE, NOVA.
        shares: Whole number of shares.
        reason: One sentence: why you are buying.
    """
    return accounts.trade(trader, "buy", ticker, shares, reason)


@mcp.tool()
def sell_shares(trader: str, ticker: str, shares: int, reason: str) -> str:
    """Sell shares you hold. Same arguments as buy_shares."""
    return accounts.trade(trader, "sell", ticker, shares, reason)


if __name__ == "__main__":
    mcp.run()
