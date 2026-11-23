"""Sara's own MCP server, built with FastMCP: her shop's tools, ready for any agent or app."""
import csv
from pathlib import Path

from mcp.server.fastmcp import FastMCP

DATA = Path(__file__).parents[1] / "data"
mcp = FastMCP("sara-shop", log_level="WARNING")  # keep the log quiet


def rows(name: str) -> list[dict]:
    with open(DATA / name) as f:
        return list(csv.DictReader(f))


@mcp.tool()
def check_stock(item: str) -> str:
    """Check how many of one product Sara's shop has in stock, and whether it needs reordering.

    Args:
        item: The product name, for example "Candle trio".
    """
    for r in rows("inventory.csv"):
        if r["item"].lower() == item.lower():
            low = int(r["in_stock"]) <= int(r["reorder_at"])
            return f"{r['item']}: {r['in_stock']} in stock (reorder at {r['reorder_at']}){', needs reordering' if low else ''}."
    return f"'{item}' is not a product in Sara's shop."


@mcp.tool()
def find_order(order_id: str) -> str:
    """Look up one customer order by its number and return its status and delivery date.

    Args:
        order_id: The order number, for example "1042".
    """
    for r in rows("orders.csv"):
        if r["order_id"] == order_id.strip("# "):
            return f"Order {r['order_id']} for {r['customer']}: {r['item']}, {r['status']}, eta {r['eta'] or 'unknown'}."
    return f"No order {order_id}."


@mcp.tool()
def low_stock() -> str:
    """List every product that is at or below its reorder level."""
    low = [r["item"] for r in rows("inventory.csv") if int(r["in_stock"]) <= int(r["reorder_at"])]
    return ", ".join(low) if low else "Nothing needs reordering."


@mcp.resource("shop://handbook")
def handbook() -> str:
    """Sara's customer service handbook: voice, products, shipping, returns."""
    return (DATA / "shop_handbook.md").read_text()


if __name__ == "__main__":
    mcp.run(transport="stdio")
