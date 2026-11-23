"""A customer chat with Microsoft Agent Framework: one tool, one session that remembers the chat."""
import asyncio
import csv
import sys
from pathlib import Path

from agent_framework import Agent
from agent_framework.openai import OpenAIChatClient
from dotenv import load_dotenv

load_dotenv(Path(__file__).parents[2] / ".env", override=True)
DATA = Path(__file__).parents[2] / "data"


def find_order(order_id: str) -> dict:
    """Look up one of Sara's orders by its number, for example "1044"."""
    with open(DATA / "orders.csv") as f:
        for row in csv.DictReader(f):
            if row["order_id"] == order_id.strip("# "):
                return {k: row[k] for k in ("order_id", "customer", "item", "status", "eta")}
    return {"error": f"No order {order_id}."}


BASE = "You answer customers of Sara's small home-goods shop. Be warm and brief. Use find_order."
CAREFUL = (" Never promise things you can't do, like watching an order or sending updates."
           " If a customer needs more help, offer to pass the message to Sara.")

agent = Agent(
    client=OpenAIChatClient(model="gpt-5.4-mini"),
    name="support",
    instructions=BASE + (CAREFUL if "--careful" in sys.argv else ""),
    tools=[find_order],
)


async def main():
    session = agent.create_session()  # one session = one customer's conversation
    for message in ["Hi, I'm Jess. Where is my order 1044?", "Okay. So what should I do now?"]:
        print(f"Customer: {message}")
        reply = await agent.run(message, session=session)
        print(f"support: {reply.text}\n")


asyncio.run(main())
