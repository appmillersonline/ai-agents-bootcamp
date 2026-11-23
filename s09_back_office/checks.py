"""Invoice processor, step 2: plain-code checks. Rules a bookkeeper would apply, with no AI in the decision."""
import json
from pathlib import Path

KNOWN = json.loads((Path(__file__).parent.parent / "data" / "known_suppliers.json").read_text())


def check(doc, seen: set) -> list[str]:
    problems = []
    key = (doc.supplier.lower(), doc.number)
    if key in seen:
        problems.append("duplicate: this invoice number was already processed")
    seen.add(key)
    if doc.subtotal is not None and doc.vat is not None and abs(doc.subtotal + doc.vat - doc.total) > 0.01:
        problems.append(f"totals don't add up: {doc.subtotal} + {doc.vat} is not {doc.total}")
    known = KNOWN.get(doc.supplier)
    if known and doc.iban and doc.iban != known["iban"]:
        problems.append("bank details changed: call the supplier before paying")
    if known and doc.total > known["usual_max"]:
        problems.append(f"unusual amount: {doc.total:.2f} is more than the usual {known['usual_max']}")
    return problems
