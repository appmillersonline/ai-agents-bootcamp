"""The digital twin app: the prompt from context.py, the tools from tools.py, and the agent loop with a chat window."""
import gradio as gr
from dotenv import load_dotenv
from openai import OpenAI

from context import NAME, SYSTEM_PROMPT
from tools import TOOLS, run_tools

load_dotenv()
client = OpenAI()
MODEL = "gpt-5.4-mini"


def chat(message, history):
    history = [{"role": h["role"], "content": h["content"]} for h in history]
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history + [{"role": "user", "content": message}]
    while True:
        response = client.chat.completions.create(model=MODEL, messages=messages, tools=TOOLS)
        reply = response.choices[0].message
        if not reply.tool_calls:
            return reply.content
        messages.append(reply)
        messages.extend(run_tools(reply.tool_calls))


EXAMPLES = ["What do you do?", "What are your strongest skills?", "Tell me about a project you're proud of.", "I'd like to work with you!"]
theme = gr.themes.Soft(primary_hue="teal", font=gr.themes.GoogleFont("Inter"))

gr.ChatInterface(chat, title=f"Chat with {NAME}'s AI twin", description="Ask me about my work, skills and projects.",
                 examples=EXAMPLES).launch(theme=theme, share=True)
