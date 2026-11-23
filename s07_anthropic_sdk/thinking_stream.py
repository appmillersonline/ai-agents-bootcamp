"""Watch Claude think, then answer: stream the thinking summary and the answer as they arrive."""
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

PROBLEM = ("Sara ships 47 mugs. A small box holds 4 mugs and costs 2.30 euros, a medium box holds 6 and costs "
           "3.20, a large box holds 10 and costs 4.90. Every mug needs its own space. What is the cheapest "
           "mix of boxes? Give the mix and the total in two lines.")

with client.messages.stream(
    model="claude-opus-5-5",
    max_tokens=16000,
    thinking={"type": "adaptive", "display": "summarized"},
    output_config={"effort": "high"},
    messages=[{"role": "user", "content": PROBLEM}],
) as stream:
    for event in stream:
        if event.type == "content_block_start":
            print("\n[thinking]" if event.content_block.type == "thinking" else "\n[answer]")
        elif event.type == "content_block_delta" and event.delta.type == "thinking_delta":
            print(event.delta.thinking, end="", flush=True)
        elif event.type == "content_block_delta" and event.delta.type == "text_delta":
            print(event.delta.text, end="", flush=True)

print(f"\n\n({stream.get_final_message().usage.output_tokens} output tokens, thinking included)")
