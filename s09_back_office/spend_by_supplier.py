"""What did Sara spend, per supplier? Plain Python on the spreadsheet, leaving out anything still in review."""
import csv
from collections import Counter
from pathlib import Path

rows = list(csv.DictReader(open(Path(__file__).parent.parent / "data" / "invoices.csv", newline="")))
spend = Counter()
for row in rows:
    if row["status"] == "ok":  # only documents that passed every check
        spend[row["supplier"]] += float(row["total"])

for supplier, total in spend.most_common():
    print(f"{supplier:<22} €{total:>8.2f}")
print(f"{'Total checked':<22} €{sum(spend.values()):>8.2f}")
waiting = [r for r in rows if r["status"] == "REVIEW"]
print(f"Waiting for Sara: {len(waiting)} documents, €{sum(float(r['total']) for r in waiting):.2f}")
