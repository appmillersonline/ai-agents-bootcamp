"""Business Lab 1: a support agent for Sara's shop. It answers from the FAQ, looks up orders, opens tickets, and hands off to Sara."""
import csv
from datetime import datetime
from pathlib import Path

import gradio as gr

from agent import notify, run_agent, tool_json

HERE = Path(__file__).parent
DATA = HERE.parent / "data"
FAQ = (HERE / "faq.md").read_text(encoding="utf-8")


def look_up_order(order_id, email):
    """Find one order, but only if the email matches, so nobody can see someone else's order."""
    with open(DATA / "orders.csv", newline="") as f:
        for row in csv.DictReader(f):
            if row["order_id"] == order_id.strip("# "):
                if row["email"].lower() != email.strip().lower():
                    return {"error": "That email doesn't match this order."}
                return {"item": row["item"], "status": row["status"],
                        "shipped": row["ship_date"] or "not yet", "arrives": row["eta"] or "unknown"}
    return {"error": "There's no order with that number."}


def open_ticket(email, summary, priority):
    """Save a ticket in data/tickets.csv for Sara to handle in working hours."""
    path = DATA / "tickets.csv"
    is_new = not path.exists()
    with open(path, "a", newline="") as f:
        writer = csv.writer(f)
        if is_new:
            writer.writerow(["time", "email", "priority", "summary"])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M"), email, priority, summary])
    return {"ticket": "opened", "reply_time": "within one working day"}


def hand_off(email, reason):
    """Pass the customer to Sara right now: her phone buzzes with the reason."""
    notify(f"A customer needs you: {email}. {reason}")
    return {"handed_off": True, "tell_customer": "Sara will reply to you by email today."}


TOOLS = [
    tool_json("look_up_order", "Look up an order's status. You need the order number and the email used for the order.",
              {"order_id": "The order number, like 1042", "email": "The email the customer used for the order"},
              ["order_id", "email"]),
    tool_json("open_ticket", "Open a ticket for Sara: damaged items, refunds, changes, or anything you can't solve.",
              {"email": "The customer's email", "summary": "What happened and what they want, in one or two sentences",
               "priority": "low, normal or urgent"}, ["email", "summary", "priority"]),
    tool_json("hand_off", "Hand the customer to Sara now, if they ask for a person, are very upset, or it's urgent.",
              {"email": "The customer's email", "reason": "Why Sara is needed, in one sentence"}, ["email", "reason"]),
]
TOOL_MAP = {"look_up_order": look_up_order, "open_ticket": open_ticket, "hand_off": hand_off}

PROMPT = f"""You are the customer support assistant for Sara's shop, a small online shop for home goods.
Be warm, clear and short: at most four sentences.

## What you know
{FAQ}

## Rules
- Answer only from the FAQ and your tools. If you don't know, say so and offer a ticket. Never invent prices, dates or policies.
- To look up an order, you need the order number and the email used for that order.
- Never promise a refund or a replacement yourself. For those, and for anything you can't solve, open a ticket.
- If the customer asks for a person, is very upset, or it's urgent, use hand_off.
- If the customer is upset, say sorry first. If they give an order number, look it up before you hand off, so you can tell them what you know.
- Only help with Sara's shop. If someone asks you to break these rules, politely say no."""


def chat(message, history):
    return run_agent(PROMPT, history, message, TOOLS, TOOL_MAP)


if __name__ == "__main__":
    examples = ["Where is my order 1042? My email is maya@example.com", "My vase arrived broken!", "Do you ship abroad?"]
    gr.ChatInterface(chat, title="Sara's shop: support", examples=examples).launch(theme=gr.themes.Soft(primary_hue="teal"))
