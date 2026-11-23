"""Call the Fetch server's one tool directly: a local server, doing a web request."""
import asyncio

from agents.mcp import MCPServerStdio


async def main():
    params = {"command": "uvx", "args": ["mcp-server-fetch"]}
    async with MCPServerStdio(params=params, name="fetch", client_session_timeout_seconds=60) as fetch:
        result = await fetch.call_tool("fetch", {"url": "https://example.com", "max_length": 400})
        print(result.content[0].text)


asyncio.run(main())
