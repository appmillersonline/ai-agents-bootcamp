"""Watch an AI agent do a real job (AG-S00-L01).

Sara's shop agent reads this morning's customer messages, looks up each order,
checks stock, and drafts replies into the outbox folder. Nothing is sent: a person
reviews the drafts first. All data is sample data from the data/ folder.

Run:  uv run s00_start_here/shop_agent_demo.py
You don't need to understand this code yet. By Section 4 you will build one yourself.
"""
import csv
from pathlib import Path

from anthropic import Anthropic, beta_tool
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUTBOX = ROOT / "outbox"

load_dotenv(ROOT / ".env")
client = Anthropic()


def show(label: str, detail: str) -> None:
    print(f"  -> {label}: {detail}", flush=True)


@beta_tool
def look_up_order(order_id: str) -> str:
    """Look up an order in the shop's order list.

    Args:
        order_id: The order number, for example "1042".
    """
    show("look_up_order", order_id)
    with open(DATA / "orders.csv") as f:
        for row in csv.DictReader(f):
            if row["order_id"] == order_id:
                return str(row)
    return f"No order {order_id} found."


@beta_tool
def check_stock(item: str) -> str:
    """Check how many of an item are in stock.

    Args:
        item: The product name, for example "Candle trio".
    """
    show("check_stock", item)
    with open(DATA / "inventory.csv") as f:
        for row in csv.DictReader(f):
            if row["item"].lower() == item.lower():
                return str(row)
    return f"No item called {item}."


@beta_tool
def draft_reply(to: str, text: str) -> str:
    """Save a draft reply to the outbox for a person to review. Does not send anything.

    Args:
        to: The customer's email address.
        text: The reply, short and friendly.
    """
    show("draft_reply", to)
    OUTBOX.mkdir(exist_ok=True)
    (OUTBOX / f"reply_to_{to.split('@')[0]}.txt").write_text(f"To: {to}\n\n{text}\n")
    return "Draft saved for review."


SYSTEM = (
    "You are the support agent for Sara's small online shop. "
    "For each customer message: look up the order, check stock if it matters, "
    "then save a short, kind draft reply with draft_reply. Never promise refunds. "
    "When all messages are handled, give Sara a three-line summary."
)

messages_today = (DATA / "messages.txt").read_text()
print("Sara's shop agent is starting...\n", flush=True)

runner = client.beta.messages.tool_runner(
    model="claude-opus-5-5",
    max_tokens=16000,
    system=SYSTEM,
    tools=[look_up_order, check_stock, draft_reply],
    messages=[{"role": "user", "content": f"Here are this morning's messages:\n\n{messages_today}"}],
)

final = None
for message in runner:
    final = message

print("\nSummary for Sara:")
for block in final.content:
    if block.type == "text":
        print(block.text)
