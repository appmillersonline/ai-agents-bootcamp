"""Chat with the digital twin in your browser: Gradio sends every message, plus the history, to chat()."""
import gradio as gr
from dotenv import load_dotenv
from openai import OpenAI

from context import SYSTEM_PROMPT

load_dotenv()
client = OpenAI()


def chat(message, history):
    history = [{"role": h["role"], "content": h["content"]} for h in history]
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history + [{"role": "user", "content": message}]
    response = client.chat.completions.create(model="gpt-5.4-mini", messages=messages)
    return response.choices[0].message.content


gr.ChatInterface(chat, title="Chat with Maya's digital twin").launch()
