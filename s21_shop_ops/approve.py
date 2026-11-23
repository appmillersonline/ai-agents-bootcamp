"""Morning: Sara reads each draft and decides. Approved drafts go to the outbox; the rest stay as drafts."""
from pathlib import Path

DRAFTS, OUTBOX = Path("drafts"), Path("outbox")
OUTBOX.mkdir(exist_ok=True)

for draft in sorted(DRAFTS.glob("*.md")):
    to, subject = draft.read_text().splitlines()[:2]
    answer = input(f"{draft.name}  {to}  |  {subject}\n  send? (y/n) ").strip().lower()
    print(f"  {answer}")
    if answer == "y":
        draft.rename(OUTBOX / draft.name)       # in a real shop: send it with your email provider here
        print("  -> outbox")
print(f"sent: {len(list(OUTBOX.glob('*.md')))}, still drafts: {len(list(DRAFTS.glob('*.md')))}")
