"""Invoice processor, step 1: read an invoice PDF or a receipt photo into clean data with structured outputs."""
import base64
import sys
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
import anthropic
from pydantic import BaseModel

load_dotenv()
client = anthropic.Anthropic()
MODEL = "claude-haiku-5-5"  # a simple job, repeated many times: the small, cheap model


class Document(BaseModel):
    kind: Literal["invoice", "receipt"]
    supplier: str
    number: str
    date: str
    subtotal: float | None
    vat: float | None
    total: float
    iban: str | None


def file_block(path: Path):
    data = base64.standard_b64encode(path.read_bytes()).decode()
    if path.suffix == ".pdf":
        return {"type": "document", "source": {"type": "base64", "media_type": "application/pdf", "data": data}}
    return {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": data}}


def read_document(path: Path):
    response = client.messages.parse(
        model=MODEL,
        max_tokens=2000,
        messages=[{"role": "user", "content": [
            file_block(path),
            {"type": "text", "text": "Copy the details of this invoice or receipt exactly as printed. "
                                     "Write dates as YYYY-MM-DD. Use null for anything that isn't on it."},
        ]}],
        output_format=Document,
    )
    return response.parsed_output, response.usage


if __name__ == "__main__":
    doc, usage = read_document(Path(sys.argv[1]))
    print(doc)
    print(f"Tokens: {usage.input_tokens} in, {usage.output_tokens} out")
