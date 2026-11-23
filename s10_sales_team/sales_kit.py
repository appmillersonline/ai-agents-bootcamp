"""The sales team's shared kit: Sara's offer, the three writers, and a test inbox for sent emails."""
import html
import json
from datetime import datetime
from pathlib import Path

from agents import Agent, function_tool
from pydantic import BaseModel

INBOX = Path(__file__).parent.parent / "outbox" / "test_inbox.json"
MODEL = "gpt-5.4-mini"

OFFER = """You write cold sales emails for Sara's shop, a small homeware shop.
New this winter: wholesale candles for cafés and boutique hotels.
Fig and cedar, hand poured, about 40 hours of burn time, 9 euros each for 24 or more.
Write one email and sign it as Sara."""


class Email(BaseModel):
    subject: str
    body: str


warm_writer = Agent(name="Warm writer", model=MODEL, output_type=Email,
                    instructions=OFFER + "\nStyle: warm and personal, like a friendly neighbour.")
witty_writer = Agent(name="Witty writer", model=MODEL, output_type=Email,
                     instructions=OFFER + "\nStyle: playful, with one light joke.")
short_writer = Agent(name="Short writer", model=MODEL, output_type=Email,
                     instructions=OFFER + "\nStyle: under 60 words, for a busy owner.")
WRITERS = [warm_writer, witty_writer, short_writer]


def send_email(to: str, subject: str, body: str) -> str:
    """Our code decides how it's delivered: today, into a test inbox page. Nothing leaves your computer."""
    emails = json.loads(INBOX.read_text()) if INBOX.exists() else []
    emails.append({"to": to, "subject": subject, "body": body, "sent": datetime.now().strftime("%H:%M")})
    INBOX.write_text(json.dumps(emails, indent=1))
    draw_inbox(emails)
    return f"Sent to {to} (test inbox)"


@function_tool
def send_email_tool(to: str, subject: str, body: str) -> str:
    """Send one email to a customer.

    Args:
        to: The customer's email address.
        subject: The subject line, without the word "Subject".
        body: The email text, ready to send.
    """
    return send_email(to, subject, body)


def draw_inbox(emails):
    rows = "".join(f"<div class='mail'><span class='time'>{e['sent']}</span><b>{html.escape(e['subject'])}</b>"
                   f"<i>to {html.escape(e['to'])}</i><p>{html.escape(e['body'])}</p></div>" for e in reversed(emails))
    style = ("body{font-family:Helvetica;background:#f3f1ec;margin:30px}.mail{background:#fff;border-radius:12px;"
             "padding:18px 22px;margin:14px 0;border-left:8px solid #e3a35e}.mail b{font-size:20px}"
             ".mail i{display:block;color:#777;margin:4px 0 10px}.mail p{white-space:pre-wrap;margin:0;line-height:1.45}"
             ".time{float:right;color:#999}")
    INBOX.with_suffix(".html").write_text(f"<html><meta charset='utf-8'><style>{style}</style>"
                                          f"<h1>Test inbox</h1>{rows}</html>")
