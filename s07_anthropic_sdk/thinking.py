"""Thinking and effort: let Claude think first, and choose how hard it thinks."""
import time

from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

PUZZLE = ("Sara sells mugs at 12 euros and vases at 30 euros. Yesterday she sold 11 items "
          "for 222 euros in total. How many vases did she sell? Answer with the number and one line why.")

for effort in ["low", "high"]:
    start = time.time()
    response = client.messages.create(
        model="claude-opus-5-5",
        max_tokens=16000,
        thinking={"type": "adaptive", "display": "summarized"},  # show a summary of the thinking
        output_config={"effort": effort},  # low, medium, high, xhigh or max
        messages=[{"role": "user", "content": PUZZLE}],
    )
    for block in response.content:
        if block.type == "thinking" and block.thinking:
            print(f"[{effort}] thought: {block.thinking.strip().splitlines()[0]}")
        elif block.type == "text":
            print(f"[{effort}] answer: {block.text}")
    print(f"[{effort}] {time.time() - start:.1f} s, {response.usage.output_tokens} output tokens\n")
