"""How to break caching by accident: put something that changes at the START of the prompt."""
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()
HANDBOOK = (Path(__file__).parent.parent / "data" / "shop_handbook.md").read_text()


def ask(system_text, question):
    response = client.messages.create(
        model="claude-opus-5-5", max_tokens=300,
        system=[{"type": "text", "text": system_text, "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": question}],
    )
    return response.usage.cache_read_input_tokens


print("Time at the START of the prompt:")
for q in ["Are mugs dishwasher safe?", "Do you ship to Norway?"]:
    start = f"Time now: {datetime.now():%H:%M:%S.%f}\n" + HANDBOOK  # changes on every call
    print(f"  read from cache: {ask(start, q)}")

print("Time moved to the END, in the question:")
for q in ["Are mugs dishwasher safe?", "Do you ship to Norway?"]:
    print(f"  read from cache: {ask(HANDBOOK, f'{q} (asked at {datetime.now():%H:%M:%S})')}")
