"""Everything about the twin's tools: what they do, how the model sees them, and how we run them safely."""
import json
import os

import requests


def notify(text):
    """Send a push notification to your phone with ntfy."""
    requests.post(f"https://ntfy.sh/{os.getenv('NTFY_TOPIC')}", data=text.encode("utf-8"))


def record_contact(email, name="not given", notes="none"):
    notify(f"New contact: {name} ({email}). Notes: {notes}")
    return {"recorded": "ok"}


def record_unknown_question(question):
    notify(f"Question I couldn't answer: {question}")
    return {"recorded": "ok"}


def tool_json(name, description, properties, required):
    params = {name: {"type": "string", "description": text} for name, text in properties.items()}
    return {"type": "function", "function": {"name": name, "description": description,
            "parameters": {"type": "object", "properties": params, "required": required}}}


TOOLS = [
    tool_json("record_contact", "Record that a visitor wants to stay in touch and gave their email address.",
              {"email": "The visitor's email", "name": "Their name, if given", "notes": "Anything useful they said"}, ["email"]),
    tool_json("record_unknown_question", "Always use this to record any question you couldn't answer.",
              {"question": "The question you couldn't answer"}, ["question"]),
]
TOOL_MAP = {"record_contact": record_contact, "record_unknown_question": record_unknown_question}


def run_tools(tool_calls):
    results = []
    for call in tool_calls:
        tool = TOOL_MAP.get(call.function.name)  # only tools we chose, nothing else
        arguments = json.loads(call.function.arguments)
        print("Tool:", call.function.name, arguments)
        result = tool(**arguments) if tool else {"error": "unknown tool"}
        results.append({"role": "tool", "tool_call_id": call.id, "content": json.dumps(result)})
    return results
