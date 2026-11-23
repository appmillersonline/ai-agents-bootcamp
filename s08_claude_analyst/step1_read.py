"""Step 1: read Sara's PDFs and answer with citations, so every claim points to a page."""
import base64

from common import DATA, MODEL, client, cost

DOCUMENTS = {"Supplier letter": "supplier_letter.pdf", "Customer survey": "customer_survey.pdf"}


def pdf_block(title, filename):
    data = base64.standard_b64encode((DATA / filename).read_bytes()).decode()
    return {"type": "document", "title": title,
            "source": {"type": "base64", "media_type": "application/pdf", "data": data},
            "citations": {"enabled": True}}  # every claim will point back to a page


def read_documents():
    response = client.messages.create(
        model=MODEL,
        max_tokens=4000,
        messages=[{"role": "user", "content": [
            *[pdf_block(title, name) for title, name in DOCUMENTS.items()],
            {"type": "text", "text": "List the key facts Sara needs for next month: price changes, deadlines, "
                                     "and what customers want. Short bullet points."},
        ]}],
    )
    facts = ""
    for block in response.content:
        if block.type == "text":
            facts += block.text
            for c in block.citations or []:  # where this sentence came from
                facts += f" [{c.document_title}, p.{c.start_page_number}]"
    return facts, response.usage


if __name__ == "__main__":
    facts, usage = read_documents()
    print(facts)
    print(f"\nStep 1 cost: ${cost(usage):.4f}")
