"""An agent loop from scratch: Claude keeps using tools until the job is done (AG-S02-L05).

Run:  uv run s02_what_agents_are/agent_loop.py
"""
import csv
import json

from anthropic import Anthropic
from dotenv import load_dotenv

load_dotenv()
client = Anthropic()


def look_up_order(order_id):
    with open("data/orders.csv") as f:
        for row in csv.DictReader(f):
            if row["order_id"] == order_id:
                return {"item": row["item"], "status": row["status"], "eta": row["eta"]}
    return {"error": "order not found"}


def check_stock(item):
    with open("data/inventory.csv") as f:
        for row in csv.DictReader(f):
            if row["item"] == item:
                return {"in_stock": int(row["in_stock"])}
    return {"error": "item not found"}


TOOLS = {"look_up_order": look_up_order, "check_stock": check_stock}
tools = [
    {"name": "look_up_order", "description": "Look up one order by its order number.",
     "input_schema": {"type": "object", "properties": {"order_id": {"type": "string"}}, "required": ["order_id"]}},
    {"name": "check_stock", "description": "Check how many of an item Sara has in stock.",
     "input_schema": {"type": "object", "properties": {"item": {"type": "string"}}, "required": ["item"]}},
]
messages = [{"role": "user", "content": "Check orders 1042, 1043 and 1044. For any order that is not shipped yet, check if its item is in stock. Then tell Sara which orders need her attention, in two short lines."}]

for step in range(1, 11):  # a safety limit: never loop forever
    response = client.messages.create(model="claude-haiku-5-5", max_tokens=800, tools=tools, messages=messages)
    if response.stop_reason != "tool_use":
        break
    messages.append({"role": "assistant", "content": response.content})
    results = []
    for block in response.content:
        if block.type == "tool_use":
            print(f"Step {step}: {block.name}({block.input})")
            output = TOOLS[block.name](**block.input)
            results.append({"type": "tool_result", "tool_use_id": block.id, "content": json.dumps(output)})
    messages.append({"role": "user", "content": results})

print(f"\nDone after {step} rounds:")
print("".join(b.text for b in response.content if b.type == "text"))
