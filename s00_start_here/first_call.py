"""Your first AI call with the Anthropic Python SDK (AG-S00-L08).

Run:  uv run s00_start_here/first_call.py
"""
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()  # reads ANTHROPIC_API_KEY from your .env file
client = Anthropic()

response = client.messages.create(
    model="claude-opus-5-5",
    max_tokens=1000,
    messages=[{"role": "user", "content": "Give me one fun fact about octopuses, in one sentence."}],
)

for block in response.content:
    if block.type == "text":
        print(block.text)
