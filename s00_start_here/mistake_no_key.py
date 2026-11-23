"""Common mistake: forgetting load_dotenv, so the key is never loaded (AG-S00-L08).

Run:  uv run s00_start_here/mistake_no_key.py
"""
from anthropic import Anthropic

client = Anthropic()  # no load_dotenv() above, so there is no key

response = client.messages.create(
    model="claude-opus-5-5",
    max_tokens=1000,
    messages=[{"role": "user", "content": "Give me one fun fact about octopuses, in one sentence."}],
)

for block in response.content:
    if block.type == "text":
        print(block.text)
