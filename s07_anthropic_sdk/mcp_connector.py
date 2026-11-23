"""MCP connector: Claude connects to a remote MCP server for you, no extra code."""
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

response = client.beta.messages.create(
    model="claude-opus-5-5",
    max_tokens=4000,
    betas=["mcp-client-2025-11-20"],
    mcp_servers=[{"type": "url", "url": "https://mcp.deepwiki.com/mcp", "name": "deepwiki"}],  # a free public server
    tools=[{"type": "mcp_toolset", "mcp_server_name": "deepwiki"}],  # let Claude use its tools
    messages=[{"role": "user", "content": "Using DeepWiki, in two sentences: what does the GitHub repo "
                                          "anthropics/anthropic-sdk-python say the tool runner does?"}],
)

for block in response.content:
    if block.type == "mcp_tool_use":
        print(f"MCP call: {block.server_name}.{block.name}")
    elif block.type == "text":
        print(block.text)
