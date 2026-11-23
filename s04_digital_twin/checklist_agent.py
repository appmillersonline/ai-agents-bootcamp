"""A visible agent loop: the model plans a checklist, then ticks off each step, like Claude Code does."""
import json

from dotenv import load_dotenv
from openai import OpenAI
from rich.console import Console

load_dotenv()
client = OpenAI()
console = Console()
steps, done = [], []


def show_checklist():
    for i, (step, ok) in enumerate(zip(steps, done), 1):
        console.print(f"[green]✔ [strike]{i}. {step}[/strike][/green]" if ok else f"☐ {i}. {step}")


def create_checklist(items):
    steps[:], done[:] = items, [False] * len(items)
    show_checklist()
    return "Checklist created"


def mark_done(number, notes):
    done[number - 1] = True
    console.print(f"\n[bold cyan]Step {number}:[/bold cyan] {notes}")
    show_checklist()
    return f"Step {number} done"


TOOLS = [
    {"type": "function", "function": {"name": "create_checklist", "description": "Plan the work as a checklist of short steps.",
     "parameters": {"type": "object", "properties": {"items": {"type": "array", "items": {"type": "string"}}}, "required": ["items"]}}},
    {"type": "function", "function": {"name": "mark_done", "description": "Tick off a step (numbered from 1) with a short note of what you found.",
     "parameters": {"type": "object", "properties": {"number": {"type": "integer"}, "notes": {"type": "string"}}, "required": ["number", "notes"]}}},
]
TOOL_MAP = {"create_checklist": create_checklist, "mark_done": mark_done}

messages = [
    {"role": "system", "content": "Solve the problem. First plan it with create_checklist, then do each step and tick it off with mark_done. Don't ask questions. End with a one-sentence answer in plain text."},
    {"role": "user", "content": "A bakery sells 120 croissants a day at 2.50 euros. Butter costs rise 20%, adding 0.15 euros per croissant. "
                                "What new price keeps the daily profit the same if they sell 10% fewer croissants? Each costs 1.10 euros to make today."},
]
while True:
    response = client.chat.completions.create(model="gpt-5.4-mini", messages=messages, tools=TOOLS)
    reply = response.choices[0].message
    if not reply.tool_calls:
        break
    messages.append(reply)
    for call in reply.tool_calls:
        result = TOOL_MAP[call.function.name](**json.loads(call.function.arguments))
        messages.append({"role": "tool", "tool_call_id": call.id, "content": result})

console.print(f"\n[bold green]Answer:[/bold green] {reply.content}")
