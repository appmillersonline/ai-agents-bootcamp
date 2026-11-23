"""One decorator turns a normal function into a tool. The S05 order lookup, now with the SDK."""
import asyncio
import csv
from pathlib import Path

from dotenv import load_dotenv
from agents import Agent, Runner, function_tool, trace

load_dotenv()
ORDERS = Path(__file__).parent.parent / "data" / "orders.csv"


@function_tool
def look_up_order(order_id: str, email: str) -> dict:
    """Look up an order's status. Only works if the email matches the order.

    Args:
        order_id: The order number, like 1042.
        email: The email the customer used for the order.
    """
    with open(ORDERS, newline="") as f:
        for row in csv.DictReader(f):
            if row["order_id"] == order_id and row["email"].lower() == email.lower():
                return {"item": row["item"], "status": row["status"], "arrives": row["eta"] or "unknown"}
    return {"error": "No order with that number and email."}


agent = Agent(
    name="Support",
    instructions="You answer questions about orders for Sara's shop. Use your tool. Never guess.",
    model="gpt-5.4-mini",
    tools=[look_up_order],
)


async def main():
    with trace("Order lookup"):
        result = await Runner.run(agent, "Where is order 1042? My email is maya@example.com")
    print(result.final_output)


asyncio.run(main())
