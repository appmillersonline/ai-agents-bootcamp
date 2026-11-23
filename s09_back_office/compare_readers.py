"""Is the cheap model good enough? Read the same invoice with Haiku and with Opus, and compare."""
from pathlib import Path

import invoice_reader
from invoice_reader import read_document

INVOICE = Path(__file__).parent.parent / "data" / "invoices" / "lumen_INV-2026-121.pdf"
PRICES = {"claude-haiku-5-5": (0.10, 0.50), "claude-opus-5-5": (4.00, 20.00)}

for model, (p_in, p_out) in PRICES.items():
    invoice_reader.MODEL = model  # swap the model the reader uses
    doc, usage = read_document(INVOICE)
    cost = usage.input_tokens * p_in / 1e6 + usage.output_tokens * p_out / 1e6
    print(f"{model:<18} ${cost:.5f}  {doc.supplier}, {doc.number}, total {doc.total}, IBAN {doc.iban}")
