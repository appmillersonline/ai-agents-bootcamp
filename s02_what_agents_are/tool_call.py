"""One tool call, by hand: Claude asks for a tool, and our code runs it (AG-S02-L04).

Run:  uv run s02_what_agents_are/tool_call.py
"""
import csv

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic()


def look_up_order(order_id):
    """Our own Python function: find one order in Sara's order file."""
    with open("data/orders.csv") as f:
        for row in csv.DictReader(f):
            if row["order_id"] == order_id:
                return row
    return {"error": "order not found"}


tools = [{
    "name": "look_up_order",
    "description": "Look up one order in Sara's shop by its order number.",
    "input_schema": {"type": "object", "properties": {"order_id": {"type": "string"}}, "required": ["order_id"]},
}]
messages = [{"role": "user", "content": "Hi, where is my order 1042?"}]

response = client.messages.create(model="claude-haiku-5-5", max_tokens=500, tools=tools, messages=messages)
print("Claude stopped because:", response.stop_reason)

for block in response.content:
    if block.type == "tool_use":
        print("Claude asks for:", block.name, block.input)
        result = look_up_order(**block.input)
        print("Our code ran it and got:", result["status"], result["eta"])
        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": [{"type": "tool_result", "tool_use_id": block.id, "content": str(result)}]})

final = client.messages.create(model="claude-haiku-5-5", max_tokens=500, tools=tools, messages=messages)
print("Claude's answer:", "".join(b.text for b in final.content if b.type == "text"))
