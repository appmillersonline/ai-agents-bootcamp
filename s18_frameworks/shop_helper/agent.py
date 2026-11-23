"""Sara's shop helper, built with Google ADK (Section 18, Lecture 1)."""
import csv
import logging
from pathlib import Path

from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

load_dotenv(Path(__file__).parents[2] / ".env", override=True)
DATA = Path(__file__).parents[2] / "data"
logging.getLogger("LiteLLM").setLevel(logging.WARNING)
MODEL = LiteLlm(model="openai/gpt-5.4-mini")


def check_stock(item: str) -> dict:
    """Check how many of one product Sara has in stock.

    Args:
        item: The product name, for example "Blue mug set".
    """
    with open(DATA / "inventory.csv") as f:
        for row in csv.DictReader(f):
            if row["item"].lower() == item.lower():
                left, reorder_at = int(row["in_stock"]), int(row["reorder_at"])
                return {"item": row["item"], "in_stock": left,
                        "needs_reorder": left <= reorder_at}
    return {"error": f"'{item}' is not a product in Sara's shop."}


def find_order(order_id: str) -> dict:
    """Look up one order by its number.

    Args:
        order_id: The order number, for example "1042".
    """
    with open(DATA / "orders.csv") as f:
        for row in csv.DictReader(f):
            if row["order_id"] == order_id.strip("# "):
                return {k: row[k] for k in ("order_id", "customer", "item", "status", "eta")}
    return {"error": f"No order {order_id}."}


orders_agent = Agent(
    name="orders_agent",
    model=MODEL,
    description="Answers questions about customer orders: status and delivery dates.",
    instruction="You track orders for Sara's shop. Use find_order. Reply in one or two friendly sentences.",
    tools=[find_order],
)

root_agent = Agent(
    name="shop_helper",
    model=MODEL,
    description="Sara's shop assistant.",
    instruction=("You help customers of Sara's small home-goods shop. "
                 "For stock questions use check_stock. "
                 "For anything about an order, hand over to orders_agent. Keep replies short."),
    tools=[check_stock],
    sub_agents=[orders_agent],
)
