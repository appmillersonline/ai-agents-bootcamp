"""Shared pieces for the Claude Analyst: the client, the model, the data folder and a cost helper."""
from pathlib import Path

from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()
MODEL = "claude-opus-5-5"
DATA = Path(__file__).parent.parent / "data"


def cost(usage) -> float:
    """Dollars for one call: Opus 5.5 is $4 per million tokens in and $20 out."""
    return usage.input_tokens * 4 / 1e6 + usage.output_tokens * 20 / 1e6
