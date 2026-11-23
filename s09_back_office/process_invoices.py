"""Invoice processor: read every invoice and receipt in the folder, check it, and write a spreadsheet plus a review list."""
import csv
from pathlib import Path

from checks import check
from invoice_reader import read_document

DATA = Path(__file__).parent.parent / "data"
seen, rows, cost = set(), [], 0.0

for path in sorted((DATA / "invoices").iterdir()):
    doc, usage = read_document(path)
    cost += usage.input_tokens * 0.10 / 1e6 + usage.output_tokens * 0.50 / 1e6  # Haiku 5.5 prices
    problems = check(doc, seen)
    status = "REVIEW" if problems else "ok"
    rows.append({**doc.model_dump(), "file": path.name, "status": status, "problems": "; ".join(problems)})
    print(f"{status:<7}{doc.supplier:<22}{doc.number:<14}{doc.total:>9.2f}  {'; '.join(problems)}")

with open(DATA / "invoices.csv", "w", newline="") as f:  # opens in Excel, Numbers or Google Sheets
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

review = [r for r in rows if r["status"] == "REVIEW"]
print(f"\n{len(rows)} documents, {len(review)} to review. Saved data/invoices.csv. Cost: ${cost:.4f}")
