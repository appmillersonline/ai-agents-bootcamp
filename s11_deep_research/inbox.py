"""The same test inbox as the AI Sales Team project: our code decides delivery, and nothing leaves your computer."""
import html
import json
from datetime import datetime
from pathlib import Path

INBOX = Path(__file__).parent.parent / "outbox" / "test_inbox.json"


def send_email(to: str, subject: str, body: str) -> str:
    INBOX.parent.mkdir(exist_ok=True)
    emails = json.loads(INBOX.read_text()) if INBOX.exists() else []
    emails.append({"to": to, "subject": subject, "body": body, "sent": datetime.now().strftime("%H:%M")})
    INBOX.write_text(json.dumps(emails, indent=1))
    rows = "".join(f"<div class='mail'><span class='time'>{e['sent']}</span><b>{html.escape(e['subject'])}</b>"
                   f"<i>to {html.escape(e['to'])}</i><p>{html.escape(e['body'])}</p></div>" for e in reversed(emails))
    style = ("body{font-family:Helvetica;background:#f3f1ec;margin:30px}.mail{background:#fff;border-radius:12px;"
             "padding:18px 22px;margin:14px 0;border-left:8px solid #e3a35e}.mail b{font-size:20px}"
             ".mail i{display:block;color:#777;margin:4px 0 10px}.mail p{white-space:pre-wrap;margin:0;line-height:1.45}"
             ".time{float:right;color:#999}")
    INBOX.with_suffix(".html").write_text(f"<html><meta charset='utf-8'><style>{style}</style><h1>Test inbox</h1>{rows}</html>")
    return f"Sent to {to} (test inbox)"
