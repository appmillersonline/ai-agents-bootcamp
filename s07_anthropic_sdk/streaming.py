"""Streaming: print Claude's answer word by word, while it is being written."""
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

with client.messages.stream(
    model="claude-opus-5-5",
    max_tokens=2000,
    messages=[{"role": "user", "content": "Write a short welcome email for new customers of Sara's pottery shop."}],
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)

final = stream.get_final_message()
print(f"\n\n({final.usage.output_tokens} tokens)")
