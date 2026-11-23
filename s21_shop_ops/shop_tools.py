"""Sara's shop tools for the nightly Shop Ops Agent (sample data, nothing really leaves the computer)."""
import csv
from datetime import date
from pathlib import Path

from claude_agent_sdk import create_sdk_mcp_server, tool

HERE = Path(__file__).parent
DATA, DRAFTS, OUTBOX = HERE / "data", HERE / "drafts", HERE / "outbox"
TODAY = date(2026, 11, 7)                      # fixed "today" so every run sees the same shop


def rows(name: str) -> list[dict]:
    return list(csv.DictReader(open(DATA / name)))


def text(s: str) -> dict:
    return {"content": [{"type": "text", "text": s}]}


@tool("low_stock", "Products at or below their reorder level, with supplier, email and pack size.", {})
async def low_stock(args):
    sup = {r["item"]: r for r in rows("suppliers.csv")}
    low = [r for r in rows("inventory.csv") if int(r["in_stock"]) <= int(r["reorder_at"])]
    return text("\n".join(f"{r['item']}: {r['in_stock']} in stock, reorder at {r['reorder_at']}, "
                          f"supplier {sup[r['item']]['supplier']} <{sup[r['item']]['email']}>, packs of {sup[r['item']]['pack_size']}"
                          for r in low) or "Nothing is low.")


@tool("late_orders", "Orders that are late today: shipped with an ETA in the past, or marked delayed.", {})
async def late_orders(args):
    late = [r for r in rows("orders.csv") if r["status"] == "delayed"
            or (r["status"] == "shipped" and r["eta"] and date.fromisoformat(r["eta"]) < TODAY)]
    return text("\n".join(f"Order {r['order_id']}: {r['customer']} <{r['email']}>, {r['item']}, "
                          f"{r['status']}, eta {r['eta'] or 'unknown'}" for r in late) or "No late orders.")


@tool("send_email", "Send an email now.", {"to": str, "subject": str, "body": str})
async def send_email(args):
    OUTBOX.mkdir(exist_ok=True)
    n = len(list(OUTBOX.glob("*.md"))) + 1
    (OUTBOX / f"{n:02d}.md").write_text(f"To: {args['to']}\nSubject: {args['subject']}\n\n{args['body']}\n")
    return text(f"Sent to {args['to']}.")


@tool("draft_email", "Save an email as a draft for Sara to approve in the morning.", {"to": str, "subject": str, "body": str})
async def draft_email(args):
    DRAFTS.mkdir(exist_ok=True)
    n = len(list(DRAFTS.glob("*.md"))) + 1
    (DRAFTS / f"{n:02d}.md").write_text(f"To: {args['to']}\nSubject: {args['subject']}\n\n{args['body']}\n")
    return text(f"Draft {n:02d} saved for Sara.")


@tool("save_report", "Save the morning report for Sara as report.md.", {"markdown": str})
async def save_report(args):
    (HERE / "report.md").write_text(args["markdown"])
    return text("Report saved.")


shop = create_sdk_mcp_server(name="shop", version="1.0.0",
                             tools=[low_stock, late_orders, send_email, draft_email, save_report])
