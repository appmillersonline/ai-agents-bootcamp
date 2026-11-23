"""Test the checks without any AI: fake documents with known problems, and the answers we expect."""
from checks import check
from invoice_reader import Document

LUMEN_IBAN = "DE00 1111 2222 3333 4444 01"


def doc(**changes):
    normal = dict(kind="invoice", supplier="Lumen Candle Co.", number="T-1", date="2026-11-01",
                  subtotal=100.0, vat=20.0, total=120.0, iban=LUMEN_IBAN)
    return Document(**{**normal, **changes})


TESTS = [
    ("a normal invoice", doc(), []),
    ("totals don't add up", doc(total=130.0), ["totals"]),
    ("new bank details", doc(iban="DE00 9999 9999 9999 9999 99"), ["bank details"]),
    ("a very big order", doc(subtotal=1000.0, vat=200.0, total=1200.0), ["unusual"]),
    ("an unknown supplier", doc(supplier="New Shop Ltd"), []),
]

passed = 0
for name, document, expected in TESTS:
    problems = check(document, set())
    ok = len(problems) == len(expected) and all(word in p for word, p in zip(expected, problems))
    passed += ok
    print(f"{'PASS' if ok else 'FAIL'}  {name:<22} {problems or 'no problems'}")
seen = set()
check(doc(), seen)
duplicate = check(doc(), seen)
passed += "duplicate" in duplicate[0]
print(f"{'PASS' if duplicate else 'FAIL'}  the same invoice twice  {duplicate}")
print(f"\n{passed} of {len(TESTS) + 1} tests passed")
