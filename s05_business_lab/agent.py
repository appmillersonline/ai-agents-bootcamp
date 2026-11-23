"""Shared pieces for the Business Lab agents: phone notifications, the tool description helper, and the agent loop."""
import json
import os

import requests
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()
MODEL = "gpt-5.4-mini"


def notify(text):
    """Send a phone notification to the business owner, with ntfy, like in Section 4."""
    requests.post(f"https://ntfy.sh/{os.getenv('NTFY_TOPIC')}", data=text.encode("utf-8"))


def tool_json(name, description, properties, required):
    params = {key: {"type": "string", "description": text} for key, text in properties.items()}
    return {"type": "function", "function": {"name": name, "description": description,
            "parameters": {"type": "object", "properties": params, "required": required}}}


def run_agent(system_prompt, history, message, tools, tool_map):
    """The agent loop from Section 4: ask the model, run the tools it asks for, repeat until it answers."""
    history = [{"role": h["role"], "content": h["content"]} for h in history]
    messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": message}]
    while True:
        response = client.chat.completions.create(model=MODEL, messages=messages, tools=tools)
        reply = response.choices[0].message
        if not reply.tool_calls:
            return reply.content
        messages.append(reply)
        for call in reply.tool_calls:
            tool = tool_map.get(call.function.name)
            arguments = json.loads(call.function.arguments)
            print("Tool:", call.function.name, arguments)
            result = tool(**arguments) if tool else {"error": "unknown tool"}
            messages.append({"role": "tool", "tool_call_id": call.id, "content": json.dumps(result)})
