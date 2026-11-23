"""Ask the API which Claude models exist, how much they can read, and how much they can write."""
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

for model in client.models.list():  # every model your key can use, newest first
    print(f"{model.id:<28} reads up to {model.max_input_tokens:>9,} tokens, writes up to {model.max_tokens:>7,}")
