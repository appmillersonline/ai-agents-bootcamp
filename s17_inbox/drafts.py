"""B9 drafts: an agent writes each reply with the facts it looks up; sending waits for Sara's OK."""
import csv
import json
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware
from langchain_core.tools import tool

load_dotenv(override=True)
ROOT = Path(__file__).parents[1]
OUTBOX = ROOT / "outbox" / "sent_replies.json"
HANDBOOK = (ROOT / "data" / "shop_handbook.md").read_text()


@tool
def lookup_order(order_id: str) -> str:
    """Look up an order's item, status, ship date and expected delivery date."""
    with open(ROOT / "data" / "orders.csv") as f:
        for row in csv.DictReader(f):
            if row["order_id"] == order_id.strip():
                return json.dumps(row)
    return f"No order {order_id} found."


@tool
def send_reply(to: str, subject: str, body: str) -> str:
    """Send a reply email to a customer or business. Sara approves every reply before it goes."""
    sent = json.loads(OUTBOX.read_text()) if OUTBOX.exists() else []
    sent.append({"to": to, "subject": subject, "body": body, "sent": datetime.now().strftime("%Y-%m-%d %H:%M")})
    OUTBOX.write_text(json.dumps(sent, indent=1))
    return f"Reply sent to {to}."


def make_drafter(checkpointer):
    return create_agent(
        model="openai:gpt-5.4-mini",
        tools=[lookup_order, send_reply],
        system_prompt=("You write short, warm replies for Sara's Shop and send them with send_reply. "
                       "Look up any order number first. Only promise what the handbook allows. Sign off as \"Sara's Shop\".\n\n"
                       f"Today is {datetime.now():%A %d %B %Y}.\n\n# Shop handbook\n{HANDBOOK}"),
        middleware=[HumanInTheLoopMiddleware(interrupt_on={"send_reply": True})],
        checkpointer=checkpointer,
    )
