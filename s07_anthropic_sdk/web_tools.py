"""Built-in web tools: Claude searches and reads the web on Anthropic's servers."""
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-5-5",
    max_tokens=8000,
    tools=[{"type": "web_search_20260209", "name": "web_search", "max_uses": 3}],  # no code needed: it runs on Anthropic's side
    messages=[{"role": "user", "content": "What do handmade ceramic vases usually sell for online? "
                                          "Give a typical price range in euros in two sentences."}],
)

sources = []
for block in response.content:
    if block.type == "server_tool_use" and block.name == "web_search":
        print("Searched:", block.input["query"])
    elif block.type == "web_search_tool_result" and isinstance(block.content, list):
        sources += [result.url for result in block.content]  # the pages it found
    elif block.type == "text":
        print(block.text, end="")
print("\n\nSources:", *sources[:3], sep="\n  ")
