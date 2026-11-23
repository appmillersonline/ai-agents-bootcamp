from triage import load_inbox, triage_all

ORDER = {"today": 0, "this_week": 1, "no_rush": 2}
emails = load_inbox()
results = triage_all(emails)

print(f"Sara's inbox: {len(emails)} emails\n")
for e, t in sorted(zip(emails, results), key=lambda pair: ORDER[pair[1].urgency]):
    reply = "reply" if t.needs_reply else "     "
    print(f"{t.urgency:9} {t.category:14} {reply}  {t.summary}")
