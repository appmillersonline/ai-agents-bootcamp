"""Two tools in one conversation: Claude decides which to use, and in what order."""
import csv
from datetime import date
from pathlib import Path

from dotenv import load_dotenv
import anthropic
from anthropic import beta_tool

load_dotenv()
client = anthropic.Anthropic()
DATA = Path(__file__).parent.parent / "data"


@beta_tool
def look_up_order(order_id: str, email: str) -> str:
    """Look up an order's status. Only works if the email matches the order.

    Args:
        order_id: The order number, like 1042.
        email: The email the customer used for the order.
    """
    print(f"  (tool) look_up_order({order_id})")
    with open(DATA / "orders.csv", newline="") as f:
        for row in csv.DictReader(f):
            if row["order_id"] == order_id and row["email"].lower() == email.lower():
                return f"{row['item']}: {row['status']}"
    return "No order with that number and email."


@beta_tool
def open_ticket(order_id: str, problem: str) -> str:
    """Open a support ticket for Sara when an order has a problem, like a damaged item.

    Args:
        order_id: The order number.
        problem: A one-line description of the problem.
    """
    print(f"  (tool) open_ticket({order_id}, {problem})")
    with open(DATA / "tickets.csv", "a", newline="") as f:
        csv.writer(f).writerow([date.today(), order_id, problem])
    return f"Ticket opened for order {order_id}. Sara replies within one working day."


runner = client.beta.messages.tool_runner(
    model="claude-opus-5-5",
    max_tokens=4000,
    system="You answer customers of Sara's shop. Check the order first, then help. Never guess. Reply in two sentences.",
    tools=[look_up_order, open_ticket],
    messages=[{"role": "user", "content": "Hi, my vase from order 1042 arrived cracked! My email is maya@example.com"}],
)
for message in runner:
    for block in message.content:
        if block.type == "text":
            print("Claude:", block.text)
