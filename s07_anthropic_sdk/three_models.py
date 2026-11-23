"""Haiku, Sonnet and Opus side by side: same job, different speed and price."""
import time

from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

PRICES = {  # dollars per million tokens: (input, output)
    "claude-haiku-5-5": (0.10, 0.50),
    "claude-sonnet-5-5": (2.00, 10.00),
    "claude-opus-5-5": (4.00, 20.00),
}
QUESTION = "Write one sentence for Sara's shop about our hand-thrown blue ceramic vase."

for model, (price_in, price_out) in PRICES.items():
    start = time.time()
    response = client.messages.create(
        model=model,
        max_tokens=1000,
        messages=[{"role": "user", "content": QUESTION}],
    )
    seconds = time.time() - start
    used = response.usage
    cost = used.input_tokens * price_in / 1e6 + used.output_tokens * price_out / 1e6
    text = next(b.text for b in response.content if b.type == "text")
    print(f"{model}  {seconds:.1f} s  ${cost:.5f}\n  {text}\n")
