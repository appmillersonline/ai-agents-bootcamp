"""Your first Claude call with the Anthropic Python SDK."""
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from .env

response = client.messages.create(
    model="claude-opus-5-5",
    max_tokens=1000,
    system="You write short, warm product descriptions for Sara's online shop.",
    messages=[{"role": "user", "content": "Describe our hand-thrown blue ceramic vase in two sentences."}],
)

print("Blocks:", [block.type for block in response.content])  # a reply is a list of blocks
for block in response.content:
    if block.type == "text":
        print(block.text)
print()
print("Stop reason:", response.stop_reason)
print("Tokens in:", response.usage.input_tokens, " out:", response.usage.output_tokens)
