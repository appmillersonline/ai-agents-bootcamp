"""Chain three AI calls: summarise a review, find its mood, then draft a reply (AG-S01-L04).

Run:  uv run s01_how_models_work/chain_review.py
"""
from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic()


def ask(prompt, model="claude-haiku-5-5"):
    """One AI call: send a prompt, get back the text of the answer."""
    response = client.messages.create(model=model, max_tokens=300, messages=[{"role": "user", "content": prompt}])
    return "".join(block.text for block in response.content if block.type == "text")


review = "The candles smell lovely, but my order took two weeks and one jar arrived cracked."

summary = ask(f"Summarise this customer review in one short line:\n{review}")
print("Summary:", summary)

mood = ask(f"Is this review happy, neutral or upset? Answer with one word.\n{summary}")
print("Mood:", mood)

reply = ask(f"Write a kind, two-sentence reply from Sara's shop to a customer whose review was {mood}. Reply with the message only.\nReview: {summary}")
print("Reply:", reply)
