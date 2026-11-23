"""Settings every agent shares. Change them here, or in your .env file."""
import os

from dotenv import load_dotenv

load_dotenv()
MODEL = os.getenv("RESEARCH_MODEL", "gpt-5.4-mini")
HOW_MANY_SEARCHES = int(os.getenv("HOW_MANY_SEARCHES", "4"))
