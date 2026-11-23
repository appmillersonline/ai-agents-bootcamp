"""A two-turn chat: Claude doesn't remember, so we send the whole conversation each time."""
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()
SYSTEM = "You write short, warm product descriptions for Sara's online shop."
messages = [{"role": "user", "content": "Describe our hand-thrown blue ceramic vase in two sentences."}]


def ask():
    response = client.messages.create(model="claude-opus-5-5", max_tokens=1000, system=SYSTEM, messages=messages)
    text = next(b.text for b in response.content if b.type == "text")
    messages.append({"role": "assistant", "content": text})  # remember Claude's answer
    return text


print("Turn 1:", ask(), "\n")
messages.append({"role": "user", "content": "Shorter, please: one sentence for Instagram."})
print("Turn 2:", ask(), "\n")
print(f"We sent {len(messages) - 1} messages the second time.")
