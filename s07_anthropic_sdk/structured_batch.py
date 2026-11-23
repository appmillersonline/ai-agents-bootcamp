"""Sort a whole inbox: the same structured form, filled in for every email, then sorted by code."""
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
    mood: Literal["happy", "neutral", "upset"]
    urgent: bool


INBOX = [
    "Hello! Are your blue mugs dishwasher safe? Thanks, Ana",
    "I want to return the tote bag from order 1041, wrong colour. Leo Park",
    "My vase (order 1042) arrived in pieces and it was a gift for tomorrow. Very disappointed. Maya Chen",
    "Order 1043 still hasn't shipped after a week. Not happy. Omar",
]

results = []
for text in INBOX:
    response = client.messages.parse(model="claude-haiku-5-5", max_tokens=1000,  # simple sorting: Haiku
                                     messages=[{"role": "user", "content": f"Read this customer email:\n{text}"}],
                                     output_format=OrderEmail)
    results.append(response.parsed_output)

for e in sorted(results, key=lambda e: (not e.urgent, e.mood != "upset")):  # urgent and upset first
    print(f"{'URGENT' if e.urgent else '      '} {e.mood:<8} {e.category:<13} {e.order_id or '-':<5} {e.customer}")
