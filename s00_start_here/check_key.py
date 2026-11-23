"""Check that your code can find your API key (AG-S00-L07).

Run:  uv run s00_start_here/check_key.py
"""
import os

from dotenv import load_dotenv

load_dotenv()  # reads your .env file
key = os.getenv("ANTHROPIC_API_KEY")

if key:
    print(f"Key found: {key[:7]}... ({len(key)} characters)")  # only the start, never the whole key
else:
    print("No key found. Check the name in .env, and that you saved the file.")
