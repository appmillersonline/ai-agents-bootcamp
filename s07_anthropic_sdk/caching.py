"""Prompt caching: send the same long handbook many times, pay full price only once."""
from pathlib import Path

from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()
HANDBOOK = (Path(__file__).parent.parent / "data" / "shop_handbook.md").read_text()

PRICE_IN = 4.00 / 1e6  # Opus 5.5: dollars per input token
QUESTIONS = ["Are the blue mugs dishwasher safe?",
             "My vase arrived cracked. What happens now?",
             "Can I use WELCOME10 and SORRY10 together?"]

for question in QUESTIONS:
    response = client.messages.create(
        model="claude-opus-5-5",
        max_tokens=1000,
        system=[{"type": "text", "text": "Answer customers of Sara's shop in one sentence, using only this handbook.\n\n" + HANDBOOK,
                 "cache_control": {"type": "ephemeral"}}],  # cache everything up to here
        messages=[{"role": "user", "content": question}],
    )
    u = response.usage
    full = (u.input_tokens + u.cache_creation_input_tokens + u.cache_read_input_tokens) * PRICE_IN
    paid = u.input_tokens * PRICE_IN + u.cache_creation_input_tokens * PRICE_IN * 1.25 + u.cache_read_input_tokens * 0.20 / 1e6
    print(f"Q: {question}")
    print(f"A: {next(b.text for b in response.content if b.type == 'text')}")
    print(f"   written to cache: {u.cache_creation_input_tokens}, read from cache: {u.cache_read_input_tokens}, "
          f"input cost ${paid:.4f} (without caching ${full:.4f})\n")
