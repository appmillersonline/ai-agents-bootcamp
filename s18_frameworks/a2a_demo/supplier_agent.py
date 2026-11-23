"""Cedar & Wick, a made-up candle maker. Their agent runs on THEIR server and speaks A2A.

Start it:  uv run uvicorn a2a_demo.supplier_agent:app --port 8001
"""
import logging

from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.adk.agents import Agent

from shop_helper.agent import MODEL

logging.getLogger("google_adk").setLevel(logging.ERROR)

CATALOG = {  # sample data: the supplier's own stock, which Sara can't see directly
    "candle trio": {"available": 40, "ships_in_days": 3, "price_each": 9.50},
    "lavender candle": {"available": 0, "ships_in_days": 14, "price_each": 5.00},
}


def check_wholesale(item: str) -> dict:
    """Check Cedar & Wick's wholesale stock for one product.

    Args:
        item: The product name, for example "Candle trio".
    """
    return CATALOG.get(item.lower(), {"error": f"Cedar & Wick doesn't make '{item}'."})


supplier_agent = Agent(
    name="cedar_and_wick",
    model=MODEL,
    description="Cedar & Wick's wholesale desk: candle stock, prices and shipping times for shops.",
    instruction="You answer wholesale questions for Cedar & Wick, a candle maker. Use check_wholesale. Be brief.",
    tools=[check_wholesale],
)

app = to_a2a(supplier_agent, port=8001)
