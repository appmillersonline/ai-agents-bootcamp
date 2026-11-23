"""Settings every agent in this section shares."""
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()
MODEL = "gpt-5.4-mini"
DATA = Path(__file__).parent.parent / "data"
