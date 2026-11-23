"""Same facts, two writers: is Sonnet good enough for step 3, at half the price?"""
from common import client
from step1_read import read_documents
from step2_chart import analyse_sales

PRICES = {"claude-opus-5-5": (4, 20), "claude-sonnet-5-5": (2, 10)}
facts, _ = read_documents()
numbers, _, _ = analyse_sales()

for model, (p_in, p_out) in PRICES.items():
    response = client.messages.create(
        model=model, max_tokens=4000,
        system="You write short monthly business reviews for Sara's shop. Use only the facts and numbers given.",
        messages=[{"role": "user", "content": f"FACTS:\n{facts}\n\nNUMBERS:\n{numbers}\n\n"
                   "Give Sara her three most important actions for November, one line each."}],
    )
    u = response.usage
    print(f"--- {model}: ${u.input_tokens * p_in / 1e6 + u.output_tokens * p_out / 1e6:.4f}")
    print(next(b.text for b in response.content if b.type == "text"), "\n")
