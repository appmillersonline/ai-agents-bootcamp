"""Give Claude a tool: the tool runner does the whole loop for you."""
import csv
from pathlib import Path

from dotenv import load_dotenv
import anthropic
from anthropic import beta_tool

load_dotenv()
client = anthropic.Anthropic()
ORDERS = Path(__file__).parent.parent / "data" / "orders.csv"


@beta_tool
def look_up_order(order_id: str, email: str) -> str:
    """Look up an order's status. Only works if the email matches the order.

    Args:
        order_id: The order number, like 1042.
        email: The email the customer used for the order.
    """
    print(f"  (tool) look_up_order({order_id}, {email})")
    with open(ORDERS, newline="") as f:
        for row in csv.DictReader(f):
            if row["order_id"] == order_id and row["email"].lower() == email.lower():
                return f"{row['item']}: {row['status']}, arrives {row['eta'] or 'unknown'}"
    return "No order with that number and email."


runner = client.beta.messages.tool_runner(
    model="claude-opus-5-5",
    max_tokens=4000,
    system="You answer customers of Sara's shop. Use your tool; never guess. Reply in one sentence.",
    tools=[look_up_order],
    messages=[{"role": "user", "content": "Where is order 1042? My email is maya@example.com"}],
)

for message in runner:  # one message per turn; the runner stops when Claude is done
    for block in message.content:
        if block.type == "text":
            print("Claude:", block.text)
