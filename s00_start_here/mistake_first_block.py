"""Common mistake: printing only the first block (AG-S00-L08).

Run:  uv run s00_start_here/mistake_first_block.py
"""
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic()

response = client.messages.create(
    model="claude-opus-5-5",
    max_tokens=1000,
    messages=[{"role": "user", "content": "Give me one fun fact about octopuses, in one sentence."}],
)

print(response.content[0].text)  # crashes: the first block is a thinking block, not text
