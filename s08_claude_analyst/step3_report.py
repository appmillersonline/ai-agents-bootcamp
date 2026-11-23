"""Step 3: put the facts and the numbers together into one report for Sara, and show what it cost."""
from common import DATA, MODEL, client, cost
from step1_read import read_documents
from step2_chart import analyse_sales

print("Step 1: reading the PDFs...")
facts, usage1 = read_documents()
print("Step 2: analysing the sales...")
numbers, chart, usage2 = analyse_sales()
print("Step 3: writing the report...")

response = client.messages.create(
    model=MODEL,
    max_tokens=4000,
    system="You write short monthly business reviews for Sara's shop. Use only the facts and numbers given. "
           "Keep every [source, page] note exactly as written. Use Markdown with clear headings.",
    messages=[{"role": "user", "content": f"FACTS FROM DOCUMENTS:\n{facts}\n\nSALES NUMBERS:\n{numbers}\n\n"
               "Write the November review: a two-line summary, the October numbers, what changes next month, "
               "and three concrete actions for Sara, each with a reason."}],
)
report = next(b.text for b in response.content if b.type == "text")
(DATA / "monthly_review.md").write_text(report + "\n\n![Revenue per item](october_chart.png)\n")

steps = {"1 Read PDFs": usage1, "2 Analyse sales": usage2, "3 Write report": response.usage}
for name, usage in steps.items():
    print(f"  {name:<16} ${cost(usage):.4f}")
print(f"  {'Total':<16} ${sum(cost(u) for u in steps.values()):.4f}")
print("Saved: data/monthly_review.md and data/october_chart.png")
