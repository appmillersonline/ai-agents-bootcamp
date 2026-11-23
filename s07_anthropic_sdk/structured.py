"""Structured outputs: get Claude's answer as a clean Python object, every time."""
from typing import Literal

from dotenv import load_dotenv
import anthropic
from pydantic import BaseModel

load_dotenv()
client = anthropic.Anthropic()


class OrderEmail(BaseModel):
    customer: str
    order_id: str | None
    category: Literal["question", "return", "damaged item", "complaint"]
    urgent: bool
    summary: str


EMAIL = """Hi, this is Omar Haddad. My candle trio (order 1043) still hasn't shipped and
I need it for my mum's birthday on Friday. Can you check? Thanks, Omar"""

response = client.messages.parse(
    model="claude-opus-5-5",
    max_tokens=4000,
    messages=[{"role": "user", "content": f"Read this customer email for Sara's shop:\n\n{EMAIL}"}],
    output_format=OrderEmail,  # the answer must fit this shape
)

email = response.parsed_output  # a real OrderEmail object, already checked
print(email)
print()
if email.urgent:
    print(f"URGENT for Sara: {email.customer}, order {email.order_id} ({email.category})")
