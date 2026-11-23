"""Runs unattended every morning: sort the inbox, write the digest, and leave every draft waiting for Sara."""
from datetime import date
from pathlib import Path

from langgraph.checkpoint.sqlite import SqliteSaver

from drafts import make_drafter
from triage import load_inbox, triage_all

ORDER = {"today": 0, "this_week": 1, "no_rush": 2}
emails = load_inbox()
results = triage_all(emails)

lines = [f"# Morning digest, {date.today():%A %d %B}", "", f"{len(emails)} new emails.", ""]
for e, t in sorted(zip(emails, results), key=lambda p: ORDER[p[1].urgency]):
    flag = "draft waiting" if t.needs_reply and t.category != "refund" else ("refund workflow" if t.category == "refund" else "")
    lines.append(f"- **{t.urgency}** · {t.category} · {t.summary} {('(' + flag + ')') if flag else ''}")
Path("morning_digest.md").write_text("\n".join(lines) + "\n")

with SqliteSaver.from_conn_string("drafts.db") as memory:
    drafter = make_drafter(memory)
    waiting = 0
    for e, t in zip(emails, results):
        if t.needs_reply and t.category != "refund":
            config = {"configurable": {"thread_id": f"{date.today()}-{e['id']}"}}
            drafter.invoke({"messages": [("user", f"Reply to this email.\nFrom: {e['from']}\nSubject: {e['subject']}\n\n{e['body']}")]}, config)
            waiting += 1
print(f"Digest written. {waiting} drafts waiting for Sara.")
