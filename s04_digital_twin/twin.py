"""The digital twin agent: two tools, and a loop that keeps going until the model has a final answer."""
import json
import os

import gradio as gr
import requests
from dotenv import load_dotenv
from openai import OpenAI

from context import SYSTEM_PROMPT

load_dotenv()
client = OpenAI()


def notify(text):
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


PROMPT = SYSTEM_PROMPT + """
- If a visitor wants to get in touch, ask for their email, then use record_contact.
- If a visitor asks about you and the answer isn't above, always use record_unknown_question."""


def chat(message, history):
    history = [{"role": h["role"], "content": h["content"]} for h in history]
    messages = [{"role": "system", "content": PROMPT}] + history + [{"role": "user", "content": message}]
    while True:
        response = client.chat.completions.create(model="gpt-5.4-mini", messages=messages, tools=TOOLS)
        reply = response.choices[0].message
        if not reply.tool_calls:
            return reply.content
        messages.append(reply)
        messages.extend(run_tools(reply.tool_calls))


gr.ChatInterface(chat, title="Chat with Maya's digital twin").launch()
