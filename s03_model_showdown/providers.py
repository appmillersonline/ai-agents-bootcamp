"""One code style for every model: the same OpenAI-style call talks to OpenAI, to Claude, and to a model on your own computer."""
import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

# Same library, three places. Only the address (base_url) and the key change.
clients = {
    "openai": OpenAI(),
    "claude": OpenAI(base_url="https://api.anthropic.com/v1/", api_key=os.getenv("ANTHROPIC_API_KEY")),
    "ollama": OpenAI(base_url="http://localhost:11434/v1", api_key="ollama"),  # local, no real key needed
}


def ask(provider, model, prompt):
    """Send one prompt to any provider, and give back the text of the answer."""
    response = clients[provider].chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    question = "In one short sentence, what's the kindest way to tell a customer their order is late?"
    print("GPT:   ", ask("openai", "gpt-5.4-nano", question))
    print("Claude:", ask("claude", "claude-haiku-5-5", question))
    print("Llama: ", ask("ollama", "llama3.2:1b", question))
