"""Web fetch: Claude reads one page you name, on Anthropic's servers, and answers from it."""
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

URL = "https://en.wikipedia.org/wiki/Stoneware"
response = client.messages.create(
    model="claude-opus-5-5",
    max_tokens=4000,
    tools=[{"type": "web_fetch_20260209", "name": "web_fetch", "max_uses": 1}],
    messages=[{"role": "user", "content": f"Read {URL} and tell Sara why stoneware suits mugs. Reply with two sentences only."}],
)

for block in response.content:
    if block.type == "server_tool_use" and block.name == "web_fetch":
        print("Fetched:", block.input["url"])
    elif block.type == "text":
        print(block.text)
