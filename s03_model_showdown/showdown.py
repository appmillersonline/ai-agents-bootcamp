"""Model Showdown: several models answer the same customer message, then an AI judge ranks them without knowing who wrote what."""
import json
import time

from providers import ask

CUSTOMER = "My candle set arrived with one jar cracked, and it's a birthday gift for tomorrow. What can you do?"
TASK = f"You reply to customers for Sara's small online candle shop. Write a reply in at most three sentences.\n\nCustomer: {CUSTOMER}"

competitors = [
    ("openai", "gpt-5.4-nano"),
    ("openai", "gpt-5.4-mini"),
    ("claude", "claude-haiku-5-5"),
    ("claude", "claude-sonnet-5-5"),
    ("ollama", "llama3.2:1b"),
]

# Round 1: every competitor answers the same task
answers = []
for provider, model in competitors:
    start = time.time()
    answer = ask(provider, model, TASK)
    print(f"{model}  ({time.time() - start:.1f} s)\n{answer}\n")
    answers.append(answer)

# Round 2: the judge sees numbered replies only, so it can't favour a brand
replies = "\n\n".join(f"Reply {i}:\n{a}" for i, a in enumerate(answers, 1))
judge_prompt = f"""You are judging replies to this customer message: {CUSTOMER}
Score each reply for kindness, a clear next step, and keeping it short.

{replies}

Answer only with JSON, best reply first: {{"ranking": [3, 1, 2], "reason": "one short sentence"}}"""

verdict = ask("claude", "claude-opus-5-5", judge_prompt)
verdict = json.loads(verdict[verdict.find("{"):verdict.rfind("}") + 1])

# Turn reply numbers back into model names, best first
names = [competitors[number - 1][1] for number in verdict["ranking"]]
print("The judge's ranking:", " > ".join(names))
print("Why:", verdict["reason"])
