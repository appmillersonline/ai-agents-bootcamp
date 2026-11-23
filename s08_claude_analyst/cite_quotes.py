"""One question, with the exact quote behind every claim: citations carry the words they point to."""
from common import MODEL, client
from step1_read import DOCUMENTS, pdf_block

response = client.messages.create(
    model=MODEL,
    max_tokens=2000,
    messages=[{"role": "user", "content": [
        *[pdf_block(title, name) for title, name in DOCUMENTS.items()],
        {"type": "text", "text": "Do customers think Sara's prices are fair? Answer in two sentences."},
    ]}],
)
for block in response.content:
    if block.type == "text":
        print(block.text, end="")
        for c in block.citations or []:
            print(f'\n    ↳ "{" ".join(c.cited_text.split())}" ({c.document_title}, p.{c.start_page_number})', end="")
print()
