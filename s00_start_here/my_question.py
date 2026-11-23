"""Your turn: the same first call, with your own question (AG-S00-L08).

Run:  uv run s00_start_here/my_question.py
"""
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic()

response = client.messages.create(
    model="claude-opus-5-5",
    max_tokens=1000,
    messages=[{"role": "user", "content": "Give me three name ideas for a small coffee shop. Reply in Spanish."}],
)

for block in response.content:
    if block.type == "text":
        print(block.text)
