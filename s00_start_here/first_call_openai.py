"""The same first AI call with the OpenAI Python SDK, if you chose OpenAI (AG-S00-L08).

Run:  uv run s00_start_here/first_call_openai.py
"""
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # reads OPENAI_API_KEY from your .env file
client = OpenAI()

response = client.responses.create(
    model="gpt-5-mini",
    input="Give me one fun fact about octopuses, in one sentence.",
)

print(response.output_text)
