"""The smallest Gradio chat: it just repeats what you type, so you can see how Gradio calls your function."""
import gradio as gr


def chat(message, history):
    return f"You said: {message}. I can see {len(history)} earlier messages."


gr.ChatInterface(chat).launch()
