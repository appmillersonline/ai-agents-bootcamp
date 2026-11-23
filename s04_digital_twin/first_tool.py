"""The twin's first tool: when a visitor leaves their email, the model asks us to send a notification to your phone."""
import json
import os

import requests
from dotenv import load_dotenv
from openai import OpenAI

from context import SYSTEM_PROMPT

load_dotenv()
client = OpenAI()


def notify(text):
    """Send a push notification to your phone with ntfy (free, no account needed)."""
    requests.post(f"https://ntfy.sh/{os.getenv('NTFY_TOPIC')}", data=text.encode("utf-8"))


def record_contact(email, name="not given"):
    notify(f"New contact: {name} ({email})")
    return {"recorded": "ok"}


# The description the model reads, so it knows the tool exists and when to use it
record_contact_json = {
    "type": "function",
    "function": {
        "name": "record_contact",
        "description": "Record that a visitor wants to stay in touch and gave their email address.",
        "parameters": {
            "type": "object",
            "properties": {
                "email": {"type": "string", "description": "The visitor's email address"},
                "name": {"type": "string", "description": "The visitor's name, if they gave it"},
            },
            "required": ["email"],
        },
    },
}

messages = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": "Loved your work! I'm Tom, tom@example.com. Let's talk about a project."},
]
response = client.chat.completions.create(model="gpt-5.4-mini", messages=messages, tools=[record_contact_json])
message = response.choices[0].message

# The model can't send anything itself: it only asks. Our code decides and runs the tool.
if message.tool_calls:
    call = message.tool_calls[0]
    arguments = json.loads(call.function.arguments)
    print("The model asked for:", call.function.name, arguments)
    print("Result:", record_contact(**arguments))
else:
    print("No tool call. The model said:", message.content)
