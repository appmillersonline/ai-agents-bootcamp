"""The same MCP server, plugged into a different framework: Google ADK instead of the OpenAI Agents SDK."""
import asyncio
import logging
from pathlib import Path

from google.adk.tools.mcp_tool.mcp_session_manager import StdioConnectionParams
from google.adk.tools.mcp_tool.mcp_toolset import McpToolset
from mcp import StdioServerParameters

logging.getLogger("google_adk").setLevel(logging.ERROR)
DATA = str(Path(__file__).parents[1] / "data")


async def main():
    files = McpToolset(connection_params=StdioConnectionParams(
        server_params=StdioServerParameters(command="npx", args=["-y", "@modelcontextprotocol/server-filesystem", DATA]),
        timeout=60))
    tools = await files.get_tools()
    print(f"Google ADK sees {len(tools)} tools from the same server: {', '.join(t.name for t in tools[:4])}, ...")
    await files.close()


asyncio.run(main())
