"""Sara's shop API: 20 endpoints (sample data). Served two ways: one tool each, or three 'explore' tools."""
import csv
import json
import sys
from pathlib import Path

from mcp.server.fastmcp import FastMCP

DATA = Path(__file__).parents[1] / "data"


def _rows(name):
    with open(DATA / name) as f:
        return list(csv.DictReader(f))


def _find(rows, key, value):
    return next((r for r in rows if r[key].lower() == str(value).lower().strip("# ")), {"error": "not found"})


ENDPOINTS = {  # name -> (description, function)
    "get_stock": ("Stock level and reorder point for one product. Args: item.", lambda item: _find(_rows("inventory.csv"), "item", item)),
    "list_stock": ("Every product with its stock level.", lambda: _rows("inventory.csv")),
    "low_stock": ("Products at or below their reorder point.", lambda: [r for r in _rows("inventory.csv") if int(r["in_stock"]) <= int(r["reorder_at"])]),
    "get_order": ("Status and delivery date of one order. Args: order_id.", lambda order_id: _find(_rows("orders.csv"), "order_id", order_id)),
    "list_orders": ("Every order with its status.", lambda: _rows("orders.csv")),
    "orders_by_status": ("Orders with one status, e.g. delayed. Args: status.", lambda status: [r for r in _rows("orders.csv") if r["status"] == status]),
    "get_customer": ("A customer's orders by name. Args: name.", lambda name: [r for r in _rows("orders.csv") if name.lower() in r["customer"].lower()]),
    "shipping_rules": ("Shipping countries, times and costs.", lambda: "Ships to the EU, UK, Norway and Switzerland; 2-3 days in Europe; free over 40 euros."),
    "returns_policy": ("Rules for returns and refunds.", lambda: "Unused items within 30 days; candles only unopened; refunds within 5 working days."),
    "damage_policy": ("What to do when an item arrives broken.", lambda: "Offer replacement or full refund; no need to return it; ask for 2 photos."),
    "product_care": ("Care instructions for mugs, vases, candles and textiles.", lambda: "Mugs: top rack. Vases: hand wash. Candles: trim wick to 5 mm."),
    "opening_hours": ("When the studio answers messages.", lambda: "Messages answered Monday to Friday, 9:00 to 17:00."),
    "gift_wrap": ("Gift wrap options and price.", lambda: "Gift wrap 3 euros per item, with a handwritten card."),
    "discount_rules": ("When discounts may be offered.", lambda: "No discounts in public review replies; 10% for wholesale over 20 items."),
    "wholesale_terms": ("Terms for shops and hotels buying in bulk.", lambda: "Minimum 20 items; invoices due in 30 days."),
    "supplier_list": ("Sara's suppliers and what they make.", lambda: "Cedar & Wick: candles. Studio: mugs, vases, totes."),
    "sales_summary": ("Total units sold last month per product.", lambda: "Sample figures only: mugs 42, vases 11, candle trios 37, totes 25."),
    "launch_info": ("Details of the next product launch.", lambda: (DATA / "launch_brief.md").read_text()[:400]),
    "review_reply_rules": ("How to reply to public reviews.", lambda: "Thank the customer, never argue, move details to email."),
    "contact_details": ("How customers can reach the shop.", lambda: "Email hello@example.com; replies within one working day."),
}

mcp = FastMCP("sara-shop-api", log_level="WARNING")

if "--progressive" in sys.argv:
    @mcp.tool()
    def search_endpoints(query: str) -> str:
        """Search Sara's shop API for endpoints that match a need. Returns names and one-line descriptions.

        Args:
            query: A few words about what you need, e.g. "order status".
        """
        words = query.lower().split()
        hits = [f"{n}: {d}" for n, (d, _) in ENDPOINTS.items() if any(w in (n + " " + d).lower() for w in words)]
        return "\n".join(hits) or "No endpoint matches. Try other words."

    @mcp.tool()
    def call_endpoint(name: str, args: str = "{}") -> str:
        """Call one endpoint found with search_endpoints.

        Args:
            name: The endpoint name, e.g. "get_order".
            args: The endpoint's arguments as JSON, e.g. {"order_id": "1044"}.
        """
        if name not in ENDPOINTS:
            return f"Unknown endpoint {name}. Use search_endpoints first."
        return json.dumps(ENDPOINTS[name][1](**json.loads(args or "{}")))
else:
    for name, (description, fn) in ENDPOINTS.items():   # flat: every endpoint is its own tool
        mcp.add_tool(fn, name=name, description=description)

if __name__ == "__main__":
    mcp.run(transport="stdio")
