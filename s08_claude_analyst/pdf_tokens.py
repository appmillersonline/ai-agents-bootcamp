"""How much does reading a PDF cost? Count the tokens before you send it."""
from pypdf import PdfReader

from common import DATA, MODEL, client
from step1_read import DOCUMENTS, pdf_block

for title, name in DOCUMENTS.items():
    count = client.messages.count_tokens(  # free: counts, doesn't run the model
        model=MODEL,
        messages=[{"role": "user", "content": [pdf_block(title, name), {"type": "text", "text": "Summarise."}]}],
    )
    pages = len(PdfReader(DATA / name).pages)
    print(f"{title:<16} {pages} page(s)  {count.input_tokens:>5} tokens  about ${count.input_tokens * 4 / 1e6:.4f} to read")
