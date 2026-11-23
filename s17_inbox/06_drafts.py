import sys
from pathlib import Path

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command

from drafts import make_drafter
from triage import load_inbox, triage_all

sys.path.append(str(Path(__file__).parents[1] / "s17_approvals"))
from approvals import make_graph as refund_workflow  # noqa: E402  (B8: refunds go through Sara's approval workflow)

emails = load_inbox()
drafter = make_drafter(InMemorySaver())
refunds = refund_workflow(InMemorySaver())

for e, t in zip(emails, triage_all(emails)):
    if not t.needs_reply:
        continue
    print(f"\n=== {e['subject']}  ({t.category}, {t.urgency})")
    if t.category == "refund":
        r = refunds.invoke({"text": e["body"]}, {"configurable": {"thread_id": f"refund-{e['id']}"}})
        print(f"Sent to the refund workflow: {r['path']}. {r['rule']}")
        continue
    config = {"configurable": {"thread_id": f"mail-{e['id']}"}}
    result = drafter.invoke({"messages": [("user", f"Reply to this email.\nFrom: {e['from']}\nSubject: {e['subject']}\n\n{e['body']}")]}, config)
    draft = result["__interrupt__"][0].value["action_requests"][0]["args"]
    print(f"Draft to {draft['to']}:\n{draft['body']}\n")
    choice = input("Send it? (y = send, e = edit, n = don't send): ").strip().lower()
    if choice == "e":
        draft = {**draft, "body": input("New reply: ")}
        decision = {"type": "edit", "edited_action": {"name": "send_reply", "args": draft}}
    elif choice == "y":
        decision = {"type": "approve"}
    else:
        decision = {"type": "reject", "message": "Sara will answer this one herself."}
    final = drafter.invoke(Command(resume={"decisions": [decision]}), config)
    print("->", "Sent." if choice in ("y", "e") else "Not sent: Sara will answer herself.")
