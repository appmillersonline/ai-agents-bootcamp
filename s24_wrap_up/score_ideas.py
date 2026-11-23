"""Score agent ideas on five questions (1 to 5 each) and rank them. The scores are my rough guesses: change them for your market."""
IDEAS = {
    # name: (pain, frequency, data ready, low risk, will pay)
    "Inbox triage for a small shop": (4, 5, 5, 4, 3),
    "Nightly stock and reorder drafts": (4, 5, 4, 4, 4),
    "Late-order customer updates": (4, 4, 5, 4, 3),
    "Sales questions in plain English": (3, 4, 4, 5, 4),
    "Company handbook Q&A": (3, 5, 5, 4, 3),
    "IT helpdesk first line": (4, 5, 4, 3, 4),
    "Clinic appointment reminders": (4, 5, 4, 3, 4),
    "Invoice data entry": (5, 5, 4, 3, 5),
    "Review replies for cafes": (3, 4, 5, 3, 2),
    "Weekly marketing report": (3, 3, 4, 5, 3),
    "Job applicant screening": (4, 3, 4, 2, 4),
    "Meeting notes to action items": (3, 5, 4, 4, 3),
    "Supplier price comparison": (3, 2, 3, 4, 3),
    "Lead research for sales": (3, 4, 3, 4, 4),
    "Social post drafts": (2, 4, 4, 4, 2),
    "Legal contract summaries": (4, 3, 4, 1, 5),
    "Tenant questions for landlords": (3, 4, 4, 3, 3),
    "School homework helper": (3, 5, 3, 2, 2),
    "Restaurant inventory counts": (4, 4, 2, 4, 3),
    "Expense report checking": (4, 4, 4, 3, 4),
    "Website bug triage": (3, 4, 4, 4, 3),
    "Event planning assistant": (2, 2, 3, 4, 3),
    "Travel booking for a team": (3, 3, 3, 2, 3),
    "Product description writer": (3, 4, 5, 4, 3),
    "Churn early warning": (5, 3, 3, 4, 5),
}
WEIGHTS = (2, 1, 1, 1, 2)                    # pain and willingness to pay count double

ranked = sorted(IDEAS.items(), key=lambda kv: -sum(w * s for w, s in zip(WEIGHTS, kv[1])))
print(f"{len(IDEAS)} ideas, max score {5 * sum(WEIGHTS)}")
for i, (name, s) in enumerate(ranked[:5], 1):
    print(f"{i}. {name:<34} {sum(w * x for w, x in zip(WEIGHTS, s))}   pain {s[0]} freq {s[1]} data {s[2]} risk {s[3]} pay {s[4]}")
print("...")
for name, s in ranked[-2:]:
    print(f"   {name:<34} {sum(w * x for w, x in zip(WEIGHTS, s))}")
